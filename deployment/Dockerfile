# Use a minimal base image with Python 3.9 installed for our application.
FROM python:3.9

# Set the working directory inside the container to /app. All subsequent commands will be relative to this directory.
WORKDIR /app

# Copy all files from the current host directory into the container's /app directory.
COPY . .

# Install Python dependencies specified in requirements.txt.
RUN pip3 install -r requirements.txt

# Create a non-root user for security best practices.
RUN useradd -m -u 1000 user
USER user

# Set environment variables for the new user, including HOME and updating PATH.
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Change the working directory to the user's application directory.
WORKDIR $HOME/app

# Copy application files, ensuring the non-root user owns them.
COPY --chown=user . $HOME/app

# Define the command to run the Streamlit app when the container starts.
# It binds to all network interfaces and disables CSRF protection for easier deployment.
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
