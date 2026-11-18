from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

	debug: bool = False
	api_v1_prefix: str = "/api/v1"
	app_name: str = "Turium AI Inbox API"
	
	secret_key: str
	chat_model: str
	database_url: str
	openai_api_key: str
	embedding_model: str

	model_config = SettingsConfigDict(
		env_file=".env",
		extra="ignore",
	)

settings = Settings()