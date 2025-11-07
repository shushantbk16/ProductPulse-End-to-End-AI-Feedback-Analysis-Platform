# Dockerfile

# 1. Start from the OFFICIAL Playwright image.
# It includes Python 3.10, Playwright, AND all the browsers.
# This is the new, correct line
FROM mcr.microsoft.com/playwright/python:v1.55.0-jammy

# 2. Set the working directory
WORKDIR /app

# 3. Copy and install *our* app's requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. We can REMOVE the "playwright install" step
# because the browsers are already in the base image.

# 5. Copy the rest of our app's code
COPY . .

# 6. Expose the port
EXPOSE 8000

# 7. Run the app
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]