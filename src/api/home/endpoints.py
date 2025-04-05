from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/home",
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def welcome_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f2f5;
            }
            
            .container {
                text-align: center;
                padding: 2rem;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            h1 {
                color: #1a73e8;
                margin-bottom: 1.5rem;
            }
            
            p {
                color: #666;
                margin-bottom: 2rem;
            }
            
            a {
                display: inline-block;
                padding: 10px 20px;
                background-color: #1a73e8;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                transition: background-color 0.3s;
            }
            
            a:hover {
                background-color: #1557b0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Our API</h1>
            <p>Thank you for using our service. Access the API documentation below:</p>
            <a href="/docs#">API Documentation</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
