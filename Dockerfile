# Dockerfile

# 1. Start from the OFFICIAL Playwright image (Uses a modern Python compatible with your requirements)
FROM mcr.microsoft.com/playwright/python:v1.55.0-jammy 
# Note: If the build fails again, try adding a comment to this line 
# to force a pull, e.g., 'FROM mcr.microsoft.com/playwright/python:v1.55.0-jammy # 2025'

# 2. Set the working directory
WORKDIR /app

# 3. Copy and install *our* app's requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of our app's code
COPY . .

# 5. Expose the port
EXPOSE 8000

# 6. Run the app
# Dockerfile (Final CMD line)
# The Gunicorn command is crashing the workers. We switch to the simpler Uvicorn command.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]