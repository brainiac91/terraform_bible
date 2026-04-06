# 3. Mastering State

Terraform state is the database of your infrastructure. It maps your code to the real world.

## The "Two-Person" Problem
Imagine you and a colleague both run `terraform apply` at the same time.
1.  You read the state.
2.  She reads the state.
3.  You add a server and write the state.
4.  She adds a database and writes the state (overwriting your changes!).

**Solution: State Locking**.
Remote backends (S3+DynamoDB, Azure Blob, Terraform Cloud) support locking. When you run `apply`, Terraform "locks" the state. If your colleague tries to run it, she gets an error:
`Error: Error acquiring the state lock`.

## Workspaces vs. Directories
A common point of confusion.

### Terraform Workspaces
Allow you to have multiple state files for the same code.
```bash
terraform workspace new dev
terraform workspace new prod
```
*   **Pros**: Quick to switch (`terraform workspace select dev`).
*   **Cons**: Dangerous. It's easy to apply "dev" changes to "prod" by forgetting to switch.
*   **Verdict**: **Avoid Workspaces for environments**. Use them for ephemeral feature branches only.

### Directory Separation (The Standard)
Use separate folders for environments.
```
/environments/dev/main.tf
/environments/prod/main.tf
```
This makes it impossible to accidentally deploy to prod.

## Hands-On: Manipulating State
Sometimes you need to refactor code without destroying infrastructure.

**Scenario**: You want to rename `random_pet.server_name` to `random_pet.app_name`.

1.  **Change the code**:
    ```hcl
    resource "random_pet" "app_name" { ... }
    ```
2.  **Run Plan**:
    Terraform sees: `- random_pet.server_name` (Destroy) and `+ random_pet.app_name` (Create).
    **This is bad!** It would change the name.

3.  **Move State**:
    ```bash
    terraform state mv random_pet.server_name random_pet.app_name
    ```

4.  **Run Plan**:
    Terraform sees: `No changes. Your infrastructure matches the configuration.`
    **Success!** You refactored the code without touching the real resource.

## Importing Existing Infrastructure
You created a file manually?
```bash
touch manual.txt
```
Add it to Terraform:
1.  Write the resource block for it.
2.  Run:
    ```bash
    terraform import local_file.manual manual.txt
    ```
Now Terraform manages it.
