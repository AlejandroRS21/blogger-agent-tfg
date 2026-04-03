# Quickstart: Frontend Web Application & Cloud Deployment

## Local Development Workflow

To run the Next.js frontend locally and verify style mimicry against the backend-generated posts:

1.  ### Generate Dummy Data (If needed)
    Run the backend batch generation script to ensure `docs/posts.json` and `docs/posts/` contain recent static data. 
    ```bash
    cd backend
    python batch_generate.py --urls <TARGET_PROFILE_URL>
    cd ..
    ```

2.  ### Install Frontend Dependencies
    Navigate to the frontend directory (named `frontend/` or working directly in root if Next.js was initialized there based on `FRONTEND_IMPLEMENTATION.md`) and install dependencies:
    ```bash
    cd frontend # (If applicable based on your Next.js setup path)
    npm install
    # or
    yarn install
    # or
    bun install
    ```

3.  ### Run the Development Server
    Boot up the React Server Components loop.
    ```bash
    npm run dev
    ```
    Visit `http://localhost:3000` to see the homepage listing all generated posts. Navigate to individual articles to verify Tailwind CSS styles successfully mimic the target design system.

## Cloud Deployment (Vercel)

The repository uses Vercel for zero-config continuous deployments. Every push to the `main` branch automatically triggers a build.

1.  ### Configuration Overrides (Optional)
    Review the `vercel.json` file in the root if custom routing or build settings were added. Normally, Next.js handles this automatically.

2.  ### Vercel CLI Testing
    If you have the Vercel CLI installed, you can simulate a production build locally before pushing:
    ```bash
    npx vercel build
    ```
    This step confirms `getStaticProps` correctly loads and parses all local content inside `docs/posts` and pre-renders the routes successfully.
