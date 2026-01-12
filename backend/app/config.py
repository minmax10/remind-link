"""
애플리케이션 설정 관리
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # 데이터베이스
    database_url: str = "sqlite:///./remindlink.db"
    
    # JWT
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OpenAI
    openai_api_key: str = ""
    
    # Anthropic (선택사항)
    anthropic_api_key: str = ""
    
    # Twitter API
    twitter_client_id: str = ""
    twitter_client_secret: str = ""
    twitter_redirect_uri: str = "http://localhost:8000/api/integrations/threads/callback"
    
    # Instagram (선택사항)
    instagram_username: str = ""
    instagram_password: str = ""
    
    # 서버
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """CORS 허용 오리진 리스트"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # 추가 필드 무시


settings = Settings()
