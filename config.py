 """
 配置加载模块
-从 config.yaml 文件加载配置，支持动态更新
+优先从 .env 文件加载配置，兼容 config.yaml，支持动态更新
 
 使用方法:
     from config import cfg
     
     # 访问配置项
     total = cfg.registration.total_accounts
     email_domain = cfg.email.domain
     
     # 或者直接导入常量（兼容旧代码）
     from config import TOTAL_ACCOUNTS, EMAIL_DOMAIN
 """
 
 import os
 import sys
 from pathlib import Path
 from dataclasses import dataclass, field
 from typing import Optional, Dict, Any
 
 # 尝试导入 yaml，如果未安装则提示
 try:
     import yaml
 except ImportError:
     print("❌ 缺少 PyYAML 依赖，请先安装:")
     print("   pip install pyyaml")
     sys.exit(1)
@@ -102,115 +102,201 @@ class CreditCardConfig:
 class PaymentConfig:
     """支付配置"""
     credit_card: CreditCardConfig = field(default_factory=CreditCardConfig)
 
 
 @dataclass
 class AppConfig:
     """应用程序完整配置"""
     registration: RegistrationConfig = field(default_factory=RegistrationConfig)
     email: EmailConfig = field(default_factory=EmailConfig)
     browser: BrowserConfig = field(default_factory=BrowserConfig)
     password: PasswordConfig = field(default_factory=PasswordConfig)
     retry: RetryConfig = field(default_factory=RetryConfig)
     batch: BatchConfig = field(default_factory=BatchConfig)
     files: FilesConfig = field(default_factory=FilesConfig)
     payment: PaymentConfig = field(default_factory=PaymentConfig)
 
 
 # ==============================================================
 # 配置加载器
 # ==============================================================
 
 class ConfigLoader:
     """
     配置加载器
-    支持从 YAML 文件加载配置，并合并默认值
+    支持从 .env / YAML 文件加载配置，并合并默认值
     """
     
     # 配置文件搜索路径（按优先级排序）
     CONFIG_FILES = [
         "config.yaml",
         "config.yml",
         "config.local.yaml",
         "config.local.yml",
     ]
+    ENV_FILES = [".env", ".env.local"]
     
     def __init__(self, config_path: Optional[str] = None):
         """
         初始化配置加载器
         
         参数:
             config_path: 指定配置文件路径，如果为 None 则自动搜索
         """
         self.config_path = config_path
         self.raw_config: Dict[str, Any] = {}
         self.config = AppConfig()
         
         self._load_config()
     
     def _find_config_file(self) -> Optional[Path]:
         """查找配置文件"""
         # 获取脚本所在目录
         base_dir = Path(__file__).parent
         
         for filename in self.CONFIG_FILES:
             config_file = base_dir / filename
             if config_file.exists():
                 return config_file
         
         return None
     
     def _load_config(self) -> None:
-        """加载配置文件"""
+        """加载配置文件（先 YAML，再由 .env 覆盖）"""
         if self.config_path:
             config_file = Path(self.config_path)
         else:
             config_file = self._find_config_file()
         
-        if config_file is None or not config_file.exists():
-            print("⚠️ 未找到配置文件 config.yaml")
-            print("   请复制 config.example.yaml 为 config.yaml 并修改配置")
-            print("   使用默认配置继续运行...")
-            return
-        
+        if config_file is not None and config_file.exists():
+            try:
+                with open(config_file, 'r', encoding='utf-8') as f:
+                    self.raw_config = yaml.safe_load(f) or {}
+
+                self.config_path = str(config_file)
+                print(f"📄 已加载配置文件: {config_file.name}")
+
+                # 解析 YAML 到数据类
+                self._parse_config()
+
+            except yaml.YAMLError as e:
+                print(f"❌ 配置文件格式错误: {e}")
+                sys.exit(1)
+            except Exception as e:
+                print(f"❌ 加载配置文件失败: {e}")
+                sys.exit(1)
+        else:
+            print("⚠️ 未找到配置文件 config.yaml，继续尝试从 .env 加载...")
+
+        # 最后应用 .env 覆盖（优先级最高）
+        self._apply_env_overrides()
+
+    def _find_env_file(self) -> Optional[Path]:
+        """查找 .env 文件"""
+        base_dir = Path(__file__).parent
+        for filename in self.ENV_FILES:
+            env_file = base_dir / filename
+            if env_file.exists():
+                return env_file
+        return None
+
+    @staticmethod
+    def _parse_dotenv(env_file: Path) -> Dict[str, str]:
+        """简易 .env 解析器（无额外依赖）"""
+        result: Dict[str, str] = {}
+        for raw_line in env_file.read_text(encoding='utf-8').splitlines():
+            line = raw_line.strip()
+            if not line or line.startswith('#') or '=' not in line:
+                continue
+            key, value = line.split('=', 1)
+            key = key.strip()
+            value = value.strip().strip('"').strip("'")
+            result[key] = value
+        return result
+
+    @staticmethod
+    def _to_int(value: Optional[str], fallback: int) -> int:
         try:
-            with open(config_file, 'r', encoding='utf-8') as f:
-                self.raw_config = yaml.safe_load(f) or {}
-            
-            self.config_path = str(config_file)
-            print(f"📄 已加载配置文件: {config_file.name}")
-            
-            # 解析配置到数据类
-            self._parse_config()
-            
-        except yaml.YAMLError as e:
-            print(f"❌ 配置文件格式错误: {e}")
-            sys.exit(1)
-        except Exception as e:
-            print(f"❌ 加载配置文件失败: {e}")
-            sys.exit(1)
+            return int(value) if value not in (None, '') else fallback
+        except (TypeError, ValueError):
+            return fallback
+
+    def _apply_env_overrides(self) -> None:
+        """应用 .env 配置覆盖"""
+        env_file = self._find_env_file()
+        dotenv_values: Dict[str, str] = {}
+        if env_file:
+            dotenv_values = self._parse_dotenv(env_file)
+            print(f"📄 已加载环境文件: {env_file.name}")
+
+        source = {**dotenv_values, **os.environ}
+
+        # 注册配置
+        self.config.registration.total_accounts = self._to_int(
+            source.get('REGISTRATION_TOTAL_ACCOUNTS'),
+            self.config.registration.total_accounts,
+        )
+        self.config.registration.min_age = self._to_int(source.get('REGISTRATION_MIN_AGE'), self.config.registration.min_age)
+        self.config.registration.max_age = self._to_int(source.get('REGISTRATION_MAX_AGE'), self.config.registration.max_age)
+
+        # 邮箱配置
+        self.config.email.worker_url = source.get('EMAIL_WORKER_URL', self.config.email.worker_url)
+        self.config.email.domain = source.get('EMAIL_DOMAIN', self.config.email.domain)
+        self.config.email.prefix_length = self._to_int(source.get('EMAIL_PREFIX_LENGTH'), self.config.email.prefix_length)
+        self.config.email.wait_timeout = self._to_int(source.get('EMAIL_WAIT_TIMEOUT'), self.config.email.wait_timeout)
+        self.config.email.poll_interval = self._to_int(source.get('EMAIL_POLL_INTERVAL'), self.config.email.poll_interval)
+        self.config.email.admin_password = source.get('EMAIL_ADMIN_PASSWORD', self.config.email.admin_password)
+
+        # 浏览器
+        self.config.browser.max_wait_time = self._to_int(source.get('BROWSER_MAX_WAIT_TIME'), self.config.browser.max_wait_time)
+        self.config.browser.short_wait_time = self._to_int(source.get('BROWSER_SHORT_WAIT_TIME'), self.config.browser.short_wait_time)
+        self.config.browser.user_agent = source.get('BROWSER_USER_AGENT', self.config.browser.user_agent)
+
+        # 密码
+        self.config.password.length = self._to_int(source.get('PASSWORD_LENGTH'), self.config.password.length)
+        self.config.password.charset = source.get('PASSWORD_CHARSET', self.config.password.charset)
+
+        # 重试
+        self.config.retry.http_max_retries = self._to_int(source.get('RETRY_HTTP_MAX_RETRIES'), self.config.retry.http_max_retries)
+        self.config.retry.http_timeout = self._to_int(source.get('RETRY_HTTP_TIMEOUT'), self.config.retry.http_timeout)
+        self.config.retry.error_page_max_retries = self._to_int(source.get('RETRY_ERROR_PAGE_MAX_RETRIES'), self.config.retry.error_page_max_retries)
+        self.config.retry.button_click_max_retries = self._to_int(source.get('RETRY_BUTTON_CLICK_MAX_RETRIES'), self.config.retry.button_click_max_retries)
+
+        # 批量
+        self.config.batch.interval_min = self._to_int(source.get('BATCH_INTERVAL_MIN'), self.config.batch.interval_min)
+        self.config.batch.interval_max = self._to_int(source.get('BATCH_INTERVAL_MAX'), self.config.batch.interval_max)
+
+        # 文件
+        self.config.files.accounts_file = source.get('FILES_ACCOUNTS_FILE', self.config.files.accounts_file)
+
+        # 支付
+        self.config.payment.credit_card.number = source.get('PAYMENT_CREDIT_CARD_NUMBER', self.config.payment.credit_card.number)
+        self.config.payment.credit_card.expiry = source.get('PAYMENT_CREDIT_CARD_EXPIRY', self.config.payment.credit_card.expiry)
+        self.config.payment.credit_card.expiry_month = source.get('PAYMENT_CREDIT_CARD_EXPIRY_MONTH', self.config.payment.credit_card.expiry_month)
+        self.config.payment.credit_card.expiry_year = source.get('PAYMENT_CREDIT_CARD_EXPIRY_YEAR', self.config.payment.credit_card.expiry_year)
+        self.config.payment.credit_card.cvc = source.get('PAYMENT_CREDIT_CARD_CVC', self.config.payment.credit_card.cvc)
     
     def _parse_config(self) -> None:
         """解析原始配置到数据类"""
         # 注册配置
         if 'registration' in self.raw_config:
             reg = self.raw_config['registration']
             self.config.registration = RegistrationConfig(
                 total_accounts=reg.get('total_accounts', 1),
                 min_age=reg.get('min_age', 20),
                 max_age=reg.get('max_age', 40)
             )
         
         # 邮箱配置
         if 'email' in self.raw_config:
             email = self.raw_config['email']
             self.config.email = EmailConfig(
                 worker_url=email.get('worker_url', ''),
                 domain=email.get('domain', ''),
                 prefix_length=email.get('prefix_length', 10),
                 wait_timeout=email.get('wait_timeout', 120),
                 poll_interval=email.get('poll_interval', 3),
                 admin_password=email.get('admin_password', '')
             )
         
         # 浏览器配置
