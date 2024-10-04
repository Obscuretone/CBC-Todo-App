# CBC Todo App

The **CBC Todo App** is a task management application designed to help users efficiently create, track, and manage their daily tasks. 

Built with React and with a Sanic API, the app features a modern and responsive interface that allows users to interact seamlessly across devices. Below are some key features and functionalities of the app:

## Key Features:

1. **User Authentication**:
   - Users can log in to their accounts using Azure Active Directory.

2. **Task Management**:
   - Users can create new tasks with titles and descriptions, which are instantly added to their task list.
   - Each task displays essential information, including its status (created or deleted) and the creation date.

3. **Dynamic Task Updates**:
   - Newly created tasks appear at the top of the task list without requiring a page refresh, enhancing the user experience.
   - A refresh button is available, allowing users to manually update their task list whenever needed.

4. **Task Deletion**:
   - Users can mark tasks as deleted, which visually grays them out and updates their status to "deleted" while keeping them in the list for reference.

5. **Intuitive User Interface**:
   - The application features a clean and modern design, making it easy to navigate and use.
   - Input fields are designed for quick task entry, with a text input for titles and a full textarea for descriptions.

7. **Responsive Design**:
   - The app is optimized for both desktop and mobile devices, providing a consistent user experience regardless of screen size.

8. **Real-time Feedback**:
   - Users receive immediate feedback when creating or deleting tasks, enhancing the overall usability of the app.

## Technical Stack:
- **Frontend**: Built using React, with Axios for API calls to manage tasks.
- **Backend**: REST API developed with Sanic, providing a fast and asynchronous server-side environment, and Redis for efficient task storage and retrieval.
- **State Management**: Utilizes React's built-in state management hooks for efficient data handling.

