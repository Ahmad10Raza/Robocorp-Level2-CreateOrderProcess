# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-11-05

### Added
- Complete end-to-end Robot Order Process automation for RobotSpareBin Industries Inc. (Robocorp Level II certification).
- Modular architecture with dedicated modules: `order_data.py`, `order_web.py`, `receipt_manager.py`, and `archiver.py`.
- Automated downloading and tabular parsing of `orders.csv` via `RPA.HTTP` and `RPA.Tables`.
- Playwright-powered web automation with dynamic selectors and modal dismissal via `robocorp.browser`.
- Resilient retry mechanism handling intermittent HTTP 500 server errors.
- HTML-to-PDF receipt generation and assembled robot screenshot embedding via `RPA.PDF`.
- Automated ZIP archiving of all PDF receipts via `RPA.Archive`.
- Sema4.ai AI Action Server interface with OpenAPI 3.1 and local MCP support.
- Dual execution support for Robocorp Tasks (RCC) and Sema4.ai Action Server.
- Unit test suite covering module logic.
