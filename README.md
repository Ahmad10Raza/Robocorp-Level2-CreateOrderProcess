# RobotSpareBin Industries Inc. - Robot Order Process
> **Robocorp Certification Level II & Sema4.ai Action Package**  
> **Framework:** Sema4.ai Actions (`sema4ai-actions`) & Robocorp Tasks (`robocorp-tasks`) with Playwright browser automation (`robocorp-browser`) and `rpaframework`.

---

## 📖 Overview
This project automates the ordering of spare parts robots for **RobotSpareBin Industries Inc.** from a CSV file. It handles intermittent 500 server errors with retry logic, produces PDF receipts with the assembled robot embedded, and bundles all receipts into a ZIP archive.

### 🔄 End-to-End Workflow
1. **Download Orders Data**: Downloads `orders.csv` from the RobotSpareBin server via `RPA.HTTP`.
2. **Parse Orders**: Loads and parses the orders using `RPA.Tables`.
3. **Web Automation**: Opens the order portal `https://robotsparebinindustries.com/#/robot-order` with `robocorp.browser`.
4. **Order Loop (per row in CSV)**:
   - Dismisses the rights disclaimer modal.
   - Fills the order form (Head dropdown, Body radio, Legs input, Shipping address).
   - Previews the assembled robot.
   - Submits the order with automatic retry on intermittent server 500 errors.
   - Stores the order receipt HTML as a PDF document.
   - Captures a screenshot of the previewed robot.
   - Embeds the screenshot into the PDF receipt using `RPA.PDF`.
   - Clicks *"Order another robot"* to reset the form.
5. **ZIP Archiving**: Packages all generated PDF receipts into `output/orders.zip` via `RPA.Archive`.

---

## 🧱 Modular Architecture

```text
CreateOrderProcess/
├── actions.py                 # Main orchestrator action/task (@action & @task)
├── config.py                  # Central configuration: URLs, paths, selectors, retries
├── modules/
│   ├── __init__.py
│   ├── order_data.py          # CSV downloading and tabular data parsing (RPA.HTTP, RPA.Tables)
│   ├── order_web.py           # Web interactions, form filling & retry submission (robocorp.browser)
│   ├── receipt_manager.py     # HTML-to-PDF receipts and screenshot watermark embedding (RPA.PDF)
│   └── archiver.py            # ZIP compression for receipts (RPA.Archive)
├── package.yaml               # Sema4.ai Action Package manifest
├── conda.yaml                 # RCC Conda environment configuration
├── robot.yaml                 # Robocorp task configuration
├── pyrightconfig.json         # Python type checking paths for VS Code
├── devdata/
│   └── input_order_robots_process.json # Local test input payload
└── tests/
    └── test_template.py       # Unit test suite
```

---

## 🚀 Execution & Testing

### 1. Run using Sema4.ai Action Server / VS Code Extension
Open the **Sema4.ai** side panel in VS Code and click **Run Action** on `order_robots_process`, or start the Action Server:
```bash
action-server start
```

### 2. Run using RCC / Robocorp Tasks
```bash
rcc run
```

### 3. Run Unit Tests
```bash
python -m unittest discover -s tests
```
