# To-Do Application Requirements

## Application Overview
- **App Name**: A To-Do application
- **Main Technologies**:
  - Backend: **Sanic**
  - Frontend: **React**
  - Database: **MariaDB** But an Azure hosted one.
  - Caching: **Memcached** But an Azure hosted one.
  - Queue: **Azure Service Bus** 
  - File Storage: **Azure Blob Storage**
  - Cloud Provider: **Azure**
  - Authentication: **Azure AD** for SSO
  - API Documentation: **OpenAPI** via `sanic-openapi`
  - Logging and Monitoring: **Azure Monitor** and **Application Insights**
  - Real-time notifications: **WebSockets** (via Azure SignalR)
  - AI integration: **Azure AI** (for task splitting)

---

## 1. Backend Requirements
- **Sanic Framework** for fast, async API endpoints
- **OpenAPI Documentation** (via `sanic-openapi`) with auto-generation and Swagger UI
- **Token-based Authentication** with **OAuth 2.0** and **JWT** tokens, using **Azure AD** for login
- **API Endpoints**:
  - `POST /tasks`: Create new tasks
  - `GET /tasks`: Retrieve all tasks (supports pagination, caching, and optional translation)
  - `GET /tasks/{id}`: Retrieve a specific task, with optional `i18n` flag
  - `PATCH /tasks/{id}`: Update a task (set as "done" or update details). Assign tasks to users or groups. Flag offensive tasks for moderation
  - `POST /tasks/{id}/split`: Split a task into two with optional AI assistance (Azure AI) 
  - `POST /groups/{group_id}/invite`: Invite users to a group (with invite confirmation)
  - `PATCH /groups/{group_id}/invite`: Confirm or reject group invite
  - `GET /admin/flagged-tasks`: Admin endpoint to view flagged tasks
  - `DELETE /users/{id}`: GDPR-compliant "forget" user data and invalidate tokens
  - **Caching**: Use **Memcached** for caching frequently accessed data (tasks, users)
  - **Queue**: Use **Azure Service Bus** for handling asynchronous operations like task splitting, email sending, etc.
- **Real-time Updates** via **WebSockets** or **Azure SignalR** to notify users of task status changes, new invites, etc.
- **Secure Connections**: Use **SSL/TLS** for encrypted connections and **Azure Key Vault** for managing secrets
- **Task Storage**: Secure task attachments stored in **Azure Blob Storage** or **S3 Equivalent**.
- **Automatic API Generation**: Swagger integration for auto-generating and serving API docs at `todo.obscuretone.com/docs`
- **Rate Limiting**: Implement rate limiting to prevent abuse.
- **MariaDB** for the primary database
  - Use a read replica to handle read-heavy traffic
  - Store tasks, users, groups, invites, flags, and translations
  - Implement **hash IDs** to avoid CRUD integrity issues (e.g., hash user emails, task name and content)
- **Secure Storage**: Encrypted task data at rest using AES encryption
- **Translation Cache**: Cache translations of tasks in the database and clear cache when tasks are edited
- **azure functions** to create a task `brew tap azure/functions` `brew install azure-functions-core-tools@4`

---

## 2. Frontend Requirements
- **React** for the frontend application
- **Login Page** with Azure AD for authentication
- **Task List View**: Display tasks with the ability to filter by group, status, and other filters
- **New Task Input**: Input field for creating tasks, including attachments and tags
- **Task Status**: Display whether tasks are pending, completed, or splitting
- **Task Split UI**: Display a visual representation when tasks are splitting and awaiting confirmation
- **Invite UI**: Invite users to groups and display their confirmation status
- **Task Group Colors**: Display tasks with color-coding based on the group ID
- **Real-time Notifications**: Use WebSockets or SignalR for notifying users of task changes and group invites
- **Task Tagging**: Implement task tagging with autocomplete for quick search and filtering
- **Cookie Consent Popup**: Display a cookie consent banner, disallow login if declined
- **Language Support**: Optional translation (with `i18n` flag) for both English and French (using Azure Translator if needed)
- **Task Attachments**: Allow users to upload files as task attachments (stored in Azure Blob Storage)
- **Status Indicators**: Show whether a task is being worked on, split, completed, etc.
- **Load More Button**: Pagination for displaying tasks in the frontend
- **Frontend Security**: Secure API requests with tokens (JWT) and manage session expiration
- **Tag Button**: Need to be able to add tags with autocomplete. The full list of tags used by a user can a call

---

## 3. Cloud Infrastructure Requirements
- **Azure AKS (Azure Kubernetes Service)** for running the app with autoscaling enabled
  - Multi-region deployment to ensure high availability and low latency
  - **Azure Load Balancer** for distributing traffic
- **Azure Blob Storage** for task attachments and file uploads
- **Azure Service Bus** or **RabbitMQ** for queuing tasks (e.g., task splitting)
- **Azure SignalR** or **WebSockets** for real-time notifications
- **Azure AD** for authentication (SSO integration with OAuth 2.0 and JWT)
- **Azure Key Vault** for securely storing sensitive data like API keys and secrets
- **Azure Monitor & Application Insights** for logging and monitoring
- **Azure API Management** to manage, monitor, and secure your API
- **Azure Blob Storage** for storing OpenGraph metadata
- **Automatic Deployment**: CI/CD pipelines using **GitHub Actions** to automate builds, tests, and deployments

---

## 4. Monitoring and Scaling
- **Auto-scaling**: Implement auto-scaling of containers in Azure Kubernetes Service (AKS)
- **Monitoring**: Use **Azure Monitor** and **Application Insights** to track:
  - Task creation rate over time
  - User logins
  - System health and API performance
- **Logging**: Log all important events (e.g., task actions, group invites, API errors)
- **Alerts**: Set up alerts for high and low thresholds (e.g., error rates, task creation spikes)

---

## 5. Testing Requirements
- **Unit Tests**: Write unit tests for the backend (e.g., using **pytest** for Python).
- **Integration Tests**: Use external scripts to perform integration tests (test APIs, database, queues).
- **Manual Testing**: Test via **Postman** or **Swagger UI**, checking all API endpoints.
- **Automated Testing**: Set up tests in **GitHub Actions** to run before each deployment and to run integration tests post deployment

---

## 7. Documentation and Version Control
- **Monorepo**: Use a single GitHub repository for both backend and frontend code.
- **Version Control**: Use **GitHub Actions** for CI/CD and automatic deployments.
- **API Docs**: Automatically generate and deploy OpenAPI documentation to `todo.obscuretone.com/docs` using **Swagger UI**.
- **GitHub Actions**: Automate the deployment process with:
  - Build and test steps
  - Deploy the backend and frontend to Azure
  - Manage container deployments and scaling in AKS

---

## 8. GDPR & Security Compliance
- **GDPR Forget Endpoint**: A `DELETE` endpoint to delete all data associated with a user (and invalidate tokens).
- **Secure Cookies**: Ensure that cookies are secure and sent over HTTPS.
- **OAuth 2.0**: Secure token-based authentication using JWT tokens and Azure AD.
- **Access Control**: Use roles and permissions for task creation, deletion, and assignment, especially for admins and group managers.

---

