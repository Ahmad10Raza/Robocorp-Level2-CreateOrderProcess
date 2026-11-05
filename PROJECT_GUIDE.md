# End-to-End Engineering Journey & Architecture Guide
## RobotSpareBin Industries Inc. - Robot Order Automation Process
> **Author:** Ahmad Raza  
> **Course:** Robocorp Certificate Level II ("Build a robot")  
> **Framework:** Sema4.ai Actions (`sema4ai-actions`) & Robocorp Tasks (`robocorp-tasks` + `robocorp-browser` + `rpaframework`)

---

## 1. Executive Summary & Objective

The objective of this project is to build a production-grade, enterprise-ready automation robot for **RobotSpareBin Industries Inc.** that fulfills customer orders for custom robots.

The automation executes the complete lifecycle:
1. Downloads an external orders dataset in CSV format.
2. Automates a modern dynamic single-page web application (`https://robotsparebinindustries.com/#/robot-order`).
3. Fills complex dynamic form controls (dropdowns, dynamic radio groups, numeric inputs, and text areas).
4. Solves real-world transient system failures (intermittent HTTP 500 server alerts).
5. Generates high-fidelity PDF receipts and captures element screenshots of assembled robots.
6. Embeds the robot screenshot into the PDF receipt as a watermark image.
7. Packages all receipts into a compressed ZIP archive for archival and compliance.
8. Exposes the entire workflow as an **AI Action** on the **Sema4.ai Action Server** with an OpenAPI 3.1 interface and local Model Context Protocol (MCP) server.

---

## 2. Thought Process & Architectural Decisions

### 2.1 Why Modular Architecture over Monolithic Scripting?
Traditional beginner tutorials often place all RPA logic inside a single 300-line `tasks.py` or `actions.py`. While quick to write, monolithic scripts fail in enterprise environments because:
- **Tight Coupling:** Web automation, PDF manipulation, and data transformation become entangled.
- **Fragile Maintenance:** A change in the website DOM breaks unrelated data-processing logic.
- **Untestable:** Unit testing individual units (like CSV validation or archiving) requires spinning up a headless browser.

### 2.2 Separation of Concerns
We partitioned the system into distinct layers:
```text
┌─────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                      │
│            actions.py (@action) / tasks.py (@task)          │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
       ┌───────▼────────┐             ┌───────▼────────┐
       │   Web Layer    │             │   Data Layer   │
       │ (order_web.py) │             │ (order_data.py)│
       └───────┬────────┘             └────────────────┘
               │
       ┌───────▼──────────────┐       ┌────────────────┐
       │   Document Layer     │──────►│ Packaging Layer│
       │(receipt_manager.py)  │       │ (archiver.py)  │
       └──────────────────────┘       └────────────────┘
               │                              │
               └──────────────┬───────────────┘
                              ▼
                     Central Configuration
                          (config.py)
```

---

## 3. Repository Structure

```text
CreateOrderProcess/
├── actions.py                 # Main Sema4.ai Action entry point (@action)
├── tasks.py                   # Main Robocorp Task entry point (@task)
├── config.py                  # Central configuration (URLs, paths, retries)
├── modules/
│   ├── __init__.py
│   ├── order_data.py          # CSV ingestion & table parsing (RPA.HTTP, RPA.Tables)
│   ├── order_web.py           # Web automation & retry submission (robocorp.browser)
│   ├── receipt_manager.py     # HTML-to-PDF receipts & image embedding (RPA.PDF)
│   └── archiver.py            # ZIP compression for receipts (RPA.Archive)
├── package.yaml               # Sema4.ai Action Package specification
├── conda_rcc.yaml             # RCC isolated environment descriptor
├── robot.yaml                 # Robocorp task definition
├── pyrightconfig.json         # Python type checking paths for VS Code / IDE
├── devdata/
│   └── input_order_robots_process.json # Local test payload
├── tests/
│   └── test_template.py       # Unit tests verifying modules
├── README.md                  # Project overview and quick start
└── PROJECT_GUIDE.md           # Comprehensive architectural & troubleshooting guide
```

---

## 4. Deep-Dive into Modular Components

### 4.1 Configuration: `config.py`
Centralizes all magic strings, endpoints, directory paths, and operational parameters:
- `ROBOT_ORDER_URL`: `https://robotsparebinindustries.com/#/robot-order`
- `ORDERS_CSV_URL`: `https://robotsparebinindustries.com/orders.csv`
- `OUTPUT_DIR`, `RECEIPTS_DIR`, `SCREENSHOTS_DIR`, `ARCHIVE_ZIP_PATH`
- `MAX_SUBMIT_RETRIES = 10`, `RETRY_DELAY_SEC = 0.5`
- `ensure_directories_exist()`: Guarantees filesystem integrity before execution.

### 4.2 Data Layer: `modules/order_data.py`
- Uses `RPA.HTTP` (`HTTP.download`) to fetch `orders.csv`.
- Uses `RPA.Tables` (`Tables.read_table_from_csv`) to parse columns into strongly-typed Python dictionaries: `Order number`, `Head`, `Body`, `Legs`, and `Address`.

### 4.3 Web Layer: `modules/order_web.py`
- **Modal Handling:** `close_annoying_modal()` uses multi-attribute selectors (`.modal button:text('OK'), .modal button:text('I guess so...')`) to dismiss the rights disclaimer.
- **Form Population:**
  - Head: `page.select_option("#head", str(order["Head"]))`
  - Body: dynamic ID interpolation `page.click(f"#id-body-{order['Body']}")`
  - Legs: placeholder-based selector `input[placeholder='Enter the part number for the legs']`
  - Address: `#address`
- **Preview:** Triggers preview and waits for `#robot-preview-image` visibility.
- **Resilient Retry Mechanism:** The RobotSpareBin backend intentionally injects random HTTP 500 errors (`.alert-danger`). `submit_order_with_retry()` loops up to 10 times, clicking `#order` and verifying `#receipt` visibility while catching transient alerts.

### 4.4 Document Layer: `modules/receipt_manager.py`
- `store_receipt_as_pdf()`: Extracts `#receipt` HTML and converts it into a PDF file via `RPA.PDF.html_to_pdf()`.
- `take_robot_screenshot()`: Takes an isolated element screenshot of `#robot-preview-image`.
- `embed_screenshot_to_receipt()`: Uses `pdf.add_watermark_image_to_pdf()` to embed the assembled robot image into the receipt in-place.

### 4.5 Archiving Layer: `modules/archiver.py`
- Uses `RPA.Archive.archive_folder_with_zip()` to package all `.pdf` receipts into `output/orders.zip`.

---

## 5. Challenges Faced & Solutions Implemented

### 🔍 Challenge 1: Local Python Environment Pollution
- **Symptom:** When running Python inside the holotree environment, Pydantic crashed with:
  `AttributeError: module 'typing_inspection.typing_objects' has no attribute 'DEPRECATED_ALIASES_IDS'`.
- **Root Cause:** Python was inheriting packages from the user's local site-packages (`~/.local/lib/python3.12/site-packages`) which had an outdated `typing-inspection (0.4.2)` conflicting with `pydantic (2.14.2)`.
- **Solution:** Enforced `PYTHONNOUSERSITE=1` across the isolated environment, preventing user-level package leakage.

---

### 🔍 Challenge 2: Action Server Decorator Conflict (`wrapper` Action Name)
- **Symptom:** Sema4.ai Action Server reported:
  `Found new action: wrapper` instead of `order_robots_process`.
- **Root Cause:** When stacking `@action` and `@task`:
  ```python
  @action
  @task
  def order_robots_process(): ...
  ```
  Python evaluated `@task` first, returning a closure named `wrapper`. Sema4.ai inspects `func.__code__.co_name` to register the action name, causing it to register as `wrapper`.
- **Solution:** Decoupled the decorators cleanly:
  - `actions.py` defines `order_robots_process` with pure `@action`.
  - `tasks.py` provides the `@task` entry point for Robocorp / RCC execution.

---

### 🔍 Challenge 3: Port Conflict on Action Server (`Errno 98`)
- **Symptom:** Starting `action-server start` crashed with:
  `[Errno 98] error while attempting to bind on address ('127.0.0.1', 8080): address already in use`.
- **Root Cause:** Port 8080 was occupied by another development service on the machine.
- **Solution:** Reconfigured the Action Server daemon to bind to port **8085**:
  ```bash
  action-server start -p 8085 --skip-lint
  ```

---

### 🔍 Challenge 4: Dual Packaging Specification Collision
- **Symptom:** Action Server attempted to bootstrap a redundant Conda environment rather than reading `package.yaml`.
- **Root Cause:** If a file named `conda.yaml` is present in the workspace root, Action Server defaults to Conda over `package.yaml`.
- **Solution:** Renamed `conda.yaml` to `conda_rcc.yaml` and updated `robot.yaml`. This allows Sema4.ai Action Server to use pure `package.yaml` while retaining full compatibility with RCC.

---

### 🔍 Challenge 5: Transient Server Errors on Order Submission
- **Symptom:** The order form randomly displays a red banner: `Something went wrong! Server returned 500`.
- **Root Cause:** Built-in challenge of Robocorp Level II testing bot resilience against flaky APIs.
- **Solution:** Implemented exponential polling with a 10-attempt retry budget in `modules/order_web.py`. The bot checks for `#receipt` visibility after each submission, retrying if `.alert-danger` is detected.

---

## 6. Execution & Verification

### Running with Action Server
1. Start the server:
   ```bash
   action-server start -p 8085 --skip-lint
   ```
2. Trigger the action via REST API:
   ```bash
   curl -X POST http://localhost:8085/api/actions/createorderprocess/order-robots-process/run \
        -H "Content-Type: application/json" \
        -d '{}'
   ```
3. Open the Web Playground: `http://localhost:8085`

### Running with Robocorp Tasks (RCC)
```bash
rcc run
```

### Running Unit Tests
```bash
python -m unittest discover -s tests
```
