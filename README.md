# Advanta SMS Integration for Odoo 18


## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)


## Overview
The Advanta SMS Integration Module enhances Odoo's messaging capabilities by integrating with Advanta's API for reliable and cost-effective SMS delivery. Whether you're sending individual messages to customers or broadcasting bulk SMS for marketing campaigns, this module provides a user-friendly interface to manage SMS accounts and send messages with ease. With a dedicated **SMS Accounts** menu for configuration and the ability to choose specific SMS accounts for each message, it’s perfect for businesses that need flexible and efficient SMS workflows.

## Features
- **Single SMS Sending**: Send individual SMS messages to customers or contacts directly through Advanta's API.
- **Bulk SMS Support**: Broadcast messages to multiple recipients at once, ideal for marketing campaigns, notifications, or alerts.
- **SMS Accounts Management**: Configure multiple Advanta SMS accounts via a dedicated **SMS Accounts** menu under the technical settings, allowing for flexible account management.
- **Account Selection for SMS**: Choose which Advanta SMS account to use when sending single or bulk SMS messages, directly from the customized SMS sending view.
- **Seamless API Integration**: Routes SMS details (phone number, message body) to Advanta's API, bypassing Odoo's native SMS system for improved performance.
- **Customizable Workflows**: Integrate SMS sending into your existing Odoo processes, such as sales, CRM, or customer support.


## Installation
1. **Download the Module**: Clone or download the module from this repository.
2. **Place in Odoo Addons**: Copy the module folder to your Odoo 18 `addons` directory.
3. **Update Module List**: In Odoo, go to **Apps** > **Update Apps List** to make the module visible.
4. **Install the Module**: Search for "Advanta SMS Integration" in the Apps menu and click **Install**.

**Dependencies**:
- Odoo 18
- Standard Odoo module: `base`

## Configuration
1. **Set Up SMS Accounts**:
   - Navigate to **Settings** > **Technical** > **SMS** > **SMS Accounts**.
   - Create a new SMS account and enter your Advanta API credentials (e.g., API key, endpoint URL, and other required details).


