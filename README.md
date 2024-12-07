# Woodworking Company API

This project is an **API for a woodworking company**, built using [FastAPI](https://fastapi.tiangolo.com/). The API will support the company's website functionalities, including managing products, contact forms, and user authentication for private sections of the site.


## Website Features

The API will power the following sections of the website:

1. **Home**
   - Display general information about the company.

2. **Products**
   - Showcase available products (optional pictures for each product).
   - Admins can add, update, or delete product details.

3. **Contact Form for New Partners**
   - Allow potential partners to submit inquiries or partnership requests.

4. **For Us**
   - Provide details about the company's history, mission, and values.

5. **Contacts and News**
   - List contact details and publish company news or updates.

6. **Sign-In Form**
   - Only authorized users will have access to private information.
   - **No Sign-Up Feature**: Account creation is restricted to admin handling.

## Technical Features

- **FastAPI Framework**: High-performance, modern web framework for building APIs with Python.
- **Authentication**:
  - Admin-only account creation.
  - Private sections of the website are accessible only to signed-in users.
- **RESTful Endpoints**: Endpoints for managing content dynamically (e.g., products, contact forms, news).
- **Image Support**: Optional image uploads for products.
- **Form Handling**: API support for processing contact form submissions.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/woodworking-company-api.git
   cd woodworking-company-api
   
2. **Create a virtual environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Run PostgreSQL in Docker (Optional)**:
   ```bash
   docker-compose up -d --build

5. **Run the application**:
   ```bash
   uvicorn main:app --reload

6. **Access the API documentation**:
  - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.
  - Open [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for ReDoc documentation.


## Future Enhancements

- Add support for multi-language content.
- Implement analytics for tracking website activity.
- Extend the API for potential mobile app integration.

## License

This project is licensed under the MIT License.

```python
# This content is formatted properly as a standalone README.md file 
# for your setup and installation instructions.
# Let me know if you need additional adjustments!
