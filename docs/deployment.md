# Local and Azure deployment

## Run locally

Install Python 3.12, Azure Functions Core Tools v4, and Azurite. From the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r src\requirements.txt
Copy-Item src\local.settings.example.json src\local.settings.json
```

In a separate terminal, start Azurite:

```powershell
azurite --location .azurite --skipApiVersionCheck
```

Start the Functions host from the `src` folder:

```powershell
Push-Location src
func start
Pop-Location
```

The frontend is configured for `http://localhost:7071` by default. Serve it at `http://localhost:8000`; the local settings file enables CORS for that origin and is ignored by Git.

The local API supports order creation, status lookup, and function-key-protected status updates. Notifications are logged when `EMAIL_MODE=log`; no email is sent.

## Create the Azure Function App

The storage account (`pavanreddysa`) must already exist in the target resource group.

1. Compile `infra/function-app.bicep` locally:

   ```powershell
   az bicep build -f infra/function-app.bicep
   ```

2. In the Azure portal, open **Deploy a custom template** → **Build your own template in the editor** → **Load file**, and select `infra/function-app.json`.
3. Deploy to the same resource group as the storage account. `functionAppName` defaults to `pavanreddyapp`; if Azure reports that name is unavailable, choose another globally unique name. Keep `storageAccountName` as `pavanreddysa`; set `frontendOrigin` to the frontend's origin (`http://localhost:8000` for local browser testing). Leave `EMAIL_MODE` as `log` for now.
4. The template creates a Flex Consumption plan, Function App, user-assigned managed identity, storage deployment container, storage data roles, and CORS setting. The deploying account needs permission to create role assignments. Check your Free Account credit before deploying.
5. After deployment, publish the Function App code from a terminal in `src`:

   ```powershell
   func azure functionapp publish <function-app-name> --build remote
   ```

   Alternatively, use the Azure Functions extension in VS Code to deploy the `src` Function App project.
6. Confirm `https://<function-app-name>.azurewebsites.net/api/health` returns `{"status":"ok"}`.
7. Replace `frontend/config.js`'s local API URL with the deployed Function App URL. If the frontend is later hosted at a different origin, update the Function App CORS allowed origin to that exact origin.

The Function App starts with `EMAIL_MODE=log`, so order notifications are recorded in logs rather than emailed. ACS email requires its endpoint, sender, and send permissions to be configured separately.
