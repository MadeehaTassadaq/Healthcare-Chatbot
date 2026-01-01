# Quickstart: Docusaurus Book Project

This guide provides the steps to set up and run the Docusaurus project locally.

## Prerequisites

- **Node.js**: Version 20.x or higher.
- **npm** (or yarn/pnpm)

## Local Development

1.  **Install Dependencies**:
    Navigate to the project root directory and run the following command to install the necessary packages defined in `package.json`.

    ```bash
    npm install
    ```

2.  **Start the Development Server**:
    After the installation is complete, start the Docusaurus development server.

    ```bash
    npm start
    ```

    This command will build the site and serve it from a local development server, typically at `http://localhost:3000`. The site will automatically reload when you make changes to the source files.

## Build for Production

To generate a static build of the website, run:

```bash
npm run build
```

The production-ready files will be placed in the `build/` directory. This is the directory that will be deployed to GitHub Pages.
