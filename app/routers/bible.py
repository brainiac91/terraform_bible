from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import markdown
import os

router = APIRouter(
    prefix="/bible",
    tags=["bible"]
)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))
CHAPTERS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "chapters")

CHAPTERS = [
    {
        "id": "01_intro",
        "title": "1. Introduction & Setup",
        "quiz": [
            {"q": "What is the key difference between Mutable and Immutable infrastructure?", "options": ["Mutable is faster", "Immutable replaces servers instead of updating them", "Mutable uses Python", "Immutable never changes"], "a": 1},
            {"q": "Which command initializes the working directory?", "options": ["terraform start", "terraform run", "terraform init", "terraform create"], "a": 2},
            {"q": "What is a Terraform Provider?", "options": ["A cloud server", "A plugin that talks to APIs", "A database", "A variable"], "a": 1}
        ],
        "flashcards": [
            {"front": "Immutable Infrastructure", "back": "The practice of replacing infrastructure rather than updating it in-place."},
            {"front": "terraform init", "back": "Initializes the directory, downloads providers, and creates the lock file."},
            {"front": "HCL", "back": "HashiCorp Configuration Language - the syntax used by Terraform."}
        ],
        "challenge": {
            "title": "The Multi-Cloud Simulator",
            "description": "Create a main.tf that uses the 'random' provider to generate a pet name, and then uses the 'local' provider to create a file named after that pet. The file content must contain the pet name in uppercase.",
            "hints": ["Use resource 'random_pet'", "Use resource 'local_file'", "Use the upper() function"],
            "solution": "resource 'random_pet' 'p' {}\nresource 'local_file' 'f' {\n  filename = '${random_pet.p.id}.txt'\n  content = upper(random_pet.p.id)\n}"
        }
    },
    {
        "id": "02_workflow",
        "title": "2. The Terraform Workflow",
        "quiz": [
            {"q": "What does 'terraform plan' do?", "options": ["Creates resources", "Deletes resources", "Previews changes", "Downloads plugins"], "a": 2},
            {"q": "Why is .terraform.lock.hcl important?", "options": ["It encrypts your state", "It pins provider versions for consistency", "It speeds up downloads", "It is not important"], "a": 1},
            {"q": "How do you fix Drift without changing infrastructure?", "options": ["terraform apply", "terraform plan -refresh-only", "terraform destroy", "terraform import"], "a": 1}
        ],
        "flashcards": [
            {"front": "Drift", "back": "When the real-world infrastructure differs from the Terraform state."},
            {"front": "terraform fmt", "back": "Automatically formats your HCL code to the canonical standard."},
            {"front": "terraform validate", "back": "Checks code for syntax errors and internal consistency."}
        ],
        "challenge": {
            "title": "The Drift Detective",
            "description": "1. Create a file with Terraform. 2. Manually delete the file in your terminal. 3. Run a command to update the state to match reality (so Terraform knows it's gone) without running 'apply'.",
            "hints": ["You need to refresh the state", "Look at 'terraform plan' flags"],
            "solution": "terraform plan -refresh-only\n(Then accept the plan)"
        }
    },
    {
        "id": "03_state",
        "title": "3. Mastering State",
        "quiz": [
            {"q": "Where is the default state stored?", "options": ["S3", "terraform.tfstate", "In memory", "On HashiCorp servers"], "a": 1},
            {"q": "What command moves a resource in state?", "options": ["terraform move", "terraform state mv", "terraform rename", "terraform mv"], "a": 1},
            {"q": "Why should you use State Locking?", "options": ["To encrypt data", "To prevent concurrent updates corrupting state", "To speed up apply", "To hide secrets"], "a": 1}
        ],
        "flashcards": [
            {"front": "terraform state list", "back": "Lists all resources currently tracked in the state file."},
            {"front": "State Locking", "back": "Prevents two people from modifying state at the same time."},
            {"front": "terraform import", "back": "Brings existing, unmanaged infrastructure into Terraform state."}
        ],
        "challenge": {
            "title": "The Refactor",
            "description": "You have a resource 'local_file.A'. Rename it in your code to 'local_file.B'. Make Terraform recognize this as a RENAME, not a destroy/create.",
            "hints": ["If you just change the code, Terraform sees a destroy/create", "You need to tell the state about the move"],
            "solution": "terraform state mv local_file.A local_file.B"
        }
    },
    {
        "id": "04_variables_outputs",
        "title": "4. Variables & Outputs",
        "quiz": [
            {"q": "How do you define a default value for a variable?", "options": ["value = ...", "default = ...", "set = ...", "input = ..."], "a": 1},
            {"q": "Which file is automatically loaded to set variables?", "options": ["vars.txt", "terraform.tfvars", "variables.tf", "input.tf"], "a": 1},
            {"q": "How do you mark an output as sensitive?", "options": ["hidden = true", "private = true", "sensitive = true", "secret = true"], "a": 2}
        ],
        "flashcards": [
            {"front": "Input Variable", "back": "Parameters to customize a module (like function arguments)."},
            {"front": "Output Value", "back": "Return values from a module (like function return values)."},
            {"front": "terraform.tfvars", "back": "The default file for assigning values to variables."}
        ],
        "challenge": {
            "title": "The Validator",
            "description": "Create a variable 'environment' that only accepts 'dev', 'staging', or 'prod'. If the user tries 'test', it must fail with a custom error message.",
            "hints": ["Use the 'validation' block", "Use the 'contains' function"],
            "solution": "variable 'environment' {\n  validation {\n    condition = contains(['dev', 'staging', 'prod'], var.environment)\n    error_message = 'Must be dev, staging, or prod'\n  }\n}"
        }
    },
    {
        "id": "05_modules",
        "title": "5. Module Architecture",
        "quiz": [
            {"q": "What is a Terraform Module?", "options": ["A plugin", "A container for multiple resources", "A database", "A variable file"], "a": 1},
            {"q": "How do you reference a module in the same directory?", "options": ["source = './module'", "source = 'local'", "import module", "include module"], "a": 0},
            {"q": "Why pin module versions?", "options": ["To save space", "To prevent breaking changes", "To speed up init", "It is required"], "a": 1}
        ],
        "flashcards": [
            {"front": "Root Module", "back": "The main directory where you run terraform commands."},
            {"front": "Child Module", "back": "A module called by another module."},
            {"front": "Module Source", "back": "The location of the module code (local path, git URL, registry)."}
        ],
        "challenge": {
            "title": "The Wrapper",
            "description": "Create a local module 'my_file' that wraps 'local_file'. It should take 'content' as input, but ALWAYS force the filename to be 'secure.txt'.",
            "hints": ["Create a folder 'modules/my_file'", "Hardcode the filename in the resource inside the module"],
            "solution": "# modules/my_file/main.tf\nresource 'local_file' 'this' {\n  filename = 'secure.txt'\n  content  = var.content\n}"
        }
    },
    {
        "id": "06_advanced_hcl",
        "title": "6. Advanced HCL Patterns",
        "quiz": [
            {"q": "What does the splat operator [*] do?", "options": ["Multiplies numbers", "Extracts a list of attributes", "Comments out code", "Deletes resources"], "a": 1},
            {"q": "Which construct creates multiple resources based on a map?", "options": ["count", "for_each", "loop", "repeat"], "a": 1},
            {"q": "What is a dynamic block used for?", "options": ["Creating dynamic resources", "Creating nested blocks (like ingress rules)", "Dynamic variables", "Dynamic outputs"], "a": 1}
        ],
        "flashcards": [
            {"front": "for_each", "back": "Iterates over a map/set to create multiple resource instances."},
            {"front": "count", "back": "Iterates over a number (0, 1, 2...) to create multiple instances."},
            {"front": "Splat [*]", "back": "Short for 'for' loop to get a list of attributes (e.g., all IP addresses)."}
        ],
        "challenge": {
            "title": "The Loop Master",
            "description": "Given a list of names ['a', 'b', 'c'], use a 'for' expression to output a list where every name is capitalized.",
            "hints": ["Use [for n in var.names : ...]", "Use the upper() function"],
            "solution": "output 'caps' {\n  value = [for n in var.names : upper(n)]\n}"
        }
    },
    {
        "id": "07_testing_validation",
        "title": "7. Testing & Validation",
        "quiz": [
            {"q": "What is the purpose of 'terraform test'?", "options": ["To test python code", "To validate infrastructure logic", "To check spelling", "To test network speed"], "a": 1},
            {"q": "What is OPA?", "options": ["Open Policy Agent", "Only Private Access", "Official Provider API", "Object Property Access"], "a": 0},
            {"q": "What does a precondition do?", "options": ["Runs before init", "Checks a condition before applying a resource", "Installs providers", "Validates variables"], "a": 1}
        ],
        "flashcards": [
            {"front": "Policy as Code", "back": "Defining security/compliance rules as code (e.g., OPA, Sentinel)."},
            {"front": "Precondition", "back": "A lifecycle block to validate assumptions about resources."},
            {"front": "Mock Provider", "back": "Simulates a provider for testing without real API calls."}
        ],
        "challenge": {
            "title": "The Gatekeeper",
            "description": "Add a precondition to a 'local_file' resource. It should only allow the creation of the file if the content is exactly 'APPROVED'.",
            "hints": ["lifecycle { precondition { ... } }", "condition = self.content == ..."],
            "solution": "lifecycle {\n  precondition {\n    condition = self.content == 'APPROVED'\n    error_message = 'Content must be APPROVED'\n  }\n}"
        }
    },
    {
        "id": "08_production",
        "title": "8. Production Best Practices",
        "quiz": [
            {"q": "Why should you NOT run apply locally in production?", "options": ["It's slow", "Lack of audit trail and consistency", "It costs money", "It requires admin rights"], "a": 1},
            {"q": "What tool estimates Terraform costs?", "options": ["TerraCost", "Infracost", "CostExplorer", "MoneyForm"], "a": 1},
            {"q": "What is Trivy used for?", "options": ["Formatting", "Security Scanning", "Cost estimation", "State management"], "a": 1}
        ],
        "flashcards": [
            {"front": "CI/CD", "back": "Continuous Integration/Deployment - Automating the apply process."},
            {"front": "Infracost", "back": "A tool to estimate cloud costs from Terraform plans."},
            {"front": "Drift Detection", "back": "Scheduled checks to ensure reality matches state."}
        ],
        "challenge": {
            "title": "The Auditor",
            "description": "Write a GitHub Actions step (pseudo-code) that runs 'terraform plan' and FAILS if there are any changes (drift detection mode).",
            "hints": ["terraform plan -detailed-exitcode", "Check the exit code"],
            "solution": "run: terraform plan -detailed-exitcode\n# If exit code is 2, there is drift -> Fail build"
        }
    }
]

import logging
import traceback

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

@router.get("/debug")
async def debug_paths():
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        content_dir = os.path.join(base_dir, "content")
        chapters_dir = os.path.join(content_dir, "chapters")
        
        return {
            "base_dir": base_dir,
            "content_dir": content_dir,
            "chapters_dir": chapters_dir,
            "chapters_exists": os.path.exists(chapters_dir),
            "files": os.listdir(chapters_dir) if os.path.exists(chapters_dir) else [],
            "templates_dir": templates.env.loader.searchpath
        }
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

@router.get("/{chapter_id}", response_class=HTMLResponse)
async def get_chapter(request: Request, chapter_id: str):
    try:
        logging.info(f"Requesting chapter: {chapter_id}")
        
        # Find current chapter index
        try:
            current_index = next(i for i, c in enumerate(CHAPTERS) if c["id"] == chapter_id)
        except StopIteration:
            logging.error(f"Chapter {chapter_id} not found in list")
            raise HTTPException(status_code=404, detail="Chapter not found")
    
        # Navigation logic
        prev_chapter = CHAPTERS[current_index - 1] if current_index > 0 else None
        next_chapter = CHAPTERS[current_index + 1] if current_index < len(CHAPTERS) - 1 else None
    
        # Load content
        file_path = os.path.join(CHAPTERS_DIR, f"{chapter_id}.md")
        logging.info(f"Looking for file at: {file_path}")
        
        if not os.path.exists(file_path):
            logging.warning(f"File not found: {file_path}")
            content = "# Content Coming Soon"
        else:
            with open(file_path, 'r') as f:
                content = f.read()
            logging.info(f"File read successfully. Length: {len(content)}")
    
        # Convert Markdown
        try:
            html_content = markdown.markdown(content, extensions=['fenced_code', 'tables'])
            logging.info("Markdown conversion successful")
        except Exception as e:
            logging.error(f"Markdown error: {e}")
            raise
    
        return templates.TemplateResponse("chapter.html", {
            "request": request,
            "content": html_content,
            "chapters": CHAPTERS,
            "current_chapter": CHAPTERS[current_index],
            "prev_chapter": prev_chapter,
            "next_chapter": next_chapter
        })
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
        logging.error(traceback.format_exc())
        return HTMLResponse(content=f"<h1>Internal Server Error</h1><pre>{traceback.format_exc()}</pre>", status_code=500)
