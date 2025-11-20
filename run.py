import uvicorn
from app import app, app_params

def main():
    uvicorn.run(app, **app_params)

if __name__ == "__main__":
    main()