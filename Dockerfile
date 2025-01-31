# Use Python as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the default Gradio port
EXPOSE 7860

# Run the Gradio app
CMD ["python", "frontend/app.py"]
