# Niva Bupa Ops CRM — Documentation

## What is this?

A web-based CRM that replaces the Excel-based Niva Bupa Ops Tracker. It manages the entire patient lifecycle from inside sales intake through coaching completion, with validated dropdowns, audit trails, and role-based access.

---

## Files in this package

| File | Purpose |
|------|---------|
| `migrate.py` | One-time script: reads the Excel file, cleans structured data, exports 3 JSON files |
| `server.py` | Python server: serves the CRM frontend and handles all read/write operations |
| `crm.html` | The CRM frontend: single HTML file with all UI and logic |
| `crm_data/patients.json` | All patient records (710 migrated from Excel) |
| `crm_data/dropdowns.json` | Dropdown validation lists (coaches, conditions, statuses, dispositions) |
| `crm_data/audit.json` | Edit history — every change logged with who/what/when |
| `crm_data/backups/` | Auto-backups of patients.json before every write (keeps last 20) |

---

## Setup (one-time)

### Step 1: Install Python dependencies

```bash
pip install fastapi uvicorn pandas openpyxl
```

### Step 2: Run the migration (if starting fresh from Excel)

```bash
python migrate.py Niva_Bupa_Ops_Tracker__5_.xlsx
```

This reads the Excel file, normalizes coach names and condition types (does NOT modify any comments/remarks), and creates the `crm_data/` folder with 3 JSON files.

You only run this once. After migration, the Excel file is no longer needed.

### Step 3: Arrange your files

```
your-folder/
├── server.py
├── crm.html
├── crm_data/
│   ├── patients.json
│   ├── dropdowns.json
│   └── audit.json
```

### Step 4: Start the server

```bash
python server.py
```

You should see:

```
==================================================
  Niva Bupa CRM Server
==================================================
  Data directory: /path/to/crm_data
  Patients: patients.json (3643 KB)
  Dropdowns: dropdowns.json
  Audit: audit.json

  Open in browser: http://localhost:8000
  For team access:  http://<your-ip>:8000
==================================================
```

### Step 5: Open in browser

Go to `http://localhost:8000`. For other team members on the same network, share `http://<your-machine-ip>:8000`.

To find your machine's IP:
- Windows: `ipconfig` → look for IPv4 Address
- Mac/Linux: `ifconfig` or `ip addr`

---

## How to use the CRM

### Role selection

At the top-right corner, select your **Role** and **User name**. The role controls which tabs you can see:

| Role | Visible tabs |
|------|-------------|
| Inside Sales | Sales Data, Dashboard |
| Health Partner (RM) | Sales Data, RM, RM Weekly, Dashboard |
| Diet Coach | Sales Data, Diet, Dashboard |
| Wellness Coach | Sales Data, Wellness, Dashboard |
| Physio Coach | Sales Data, Physio, Dashboard |
| CS Agent | All tabs except Coaches |
| Admin (All Access) | All tabs |

### Tab: Sales Data

This is where Inside Sales adds new patients.

**Adding a new patient:**
1. Click the **"+ Add new patient"** button (top-right of filter bar)
2. Fill in all required fields (marked with red asterisk): Patient Name, Contact Number, Condition Type, Plan Duration, Plan Price, Plan Purchase Date
3. Click **"Save & create patient"**
4. The patient automatically appears in all other tabs (RM, Diet, Wellness, Physio, Weekly) with empty operational fields

**Editing a patient's seed data:**
1. Click any row in the table, or click the **"Edit"** button
2. Modify the fields in the side panel
3. Click **"Save changes"**

### Tab: RM

This is the Health Partner's workspace for welcome calls and coach assignments.

**Logging a welcome call attempt:**
1. Click a patient row to open the side panel
2. Scroll to "Welcome call attempts"
3. Click **"+ Log new attempt"**
4. Date and time auto-fill to right now
5. Select a Disposition from the dropdown (Completed, Partially Completed, No answer, etc.)
6. Add optional remarks
7. Click **"Add attempt"**

**Assigning coaches:**
1. In the side panel, scroll to "Coach assignment"
2. Select Diet Coach, Wellness Coach, and Physio Coach from the dropdowns
3. Add appointment remarks if needed (e.g., "Michelle - 3:30PM (19/7/2025)")
4. Click **"Save changes"**

**Updating WC status and other fields:**
1. Change Health Partner, WC Done (Yes/No), WC Completion Date, Metabolic Assessment from their respective dropdowns
2. Add remarks in the free-text area
3. Click **"Save changes"**

### Tab: Diet / Wellness / Physio

These tabs work identically (with minor differences in fields).

**Viewing monthly progress:**
- The table shows M1-M6 columns (or M1+M4 for Physio) with status icons: ✓ (completed), ✗ (inactive), ⏳ (pending), — (not started)
- Click any patient row to open the monthly detail panel

**Logging a monthly assessment attempt:**
1. Click a patient row
2. In the monthly cycle section, click the month tab you want (M1, M2, etc.)
3. Click **"+ Log attempt"**
4. Fill in date, time, disposition
5. Click **"Add attempt"**

**Updating coach and status:**
1. Change the Coach dropdown at the top of the side panel
2. Change the Status dropdown
3. Update the "Current status notes" text area
4. Click **"Save changes"**

### Tab: RM Weekly

For ongoing RM follow-ups after onboarding.

**Logging a weekly entry:**
1. Click a patient row
2. The side panel shows the full weekly history
3. At the bottom, the next week number is auto-calculated
4. Fill in date and remarks
5. Click **"Save entry"**

### Tab: Coaches

For managing the master list of coaches.

**Adding a new coach:**
1. Click **"+ Add new coach"**
2. Enter the coach's name
3. Select their type (Diet, Wellness, Physio, or HP/RM)
4. Click **"Add coach"**
5. The new name immediately appears in all dropdowns across the CRM

### Tab: Dashboard

Shows KPI cards and charts calculated from live data: total patients, WC completion rate, active/inactive counts, condition distribution, and coach workload.

---

## What was cleaned during migration

The migration script normalizes only structured fields. All free-text fields (remarks, comments, notes, current status) are preserved exactly as they were in the Excel.

### Coach name normalization

| Dirty value (from Excel) | Cleaned to |
|--------------------------|------------|
| bhakti | Bhakti |
| BHUVANESWARI, Bhuvaneswari | Bhuvaneshwari |
| Swetha.K | Swetha K |
| Dr.Radhika/Vandna | Radhika |
| shubha, Shubha, Shubha dubey | Shubha Dubey |
| shobika | Shobika |
| sridurga | Sridurga |
| Manya Jain | Manya |
| Ishwarya | Iswarya |
| sakshi | Sakshi |
| No coach Assigned | (set to empty — not a coach name) |

### Other normalizations

| Field | What was fixed |
|-------|---------------|
| Condition Type | "cholesterol" → "Cholesterol" |
| Plan Duration | "3 months" → "3 Months", "6 Months " (trailing space) → "6 Months", "1 year" → "12 Months" |
| Dates | All converted to YYYY-MM-DD format |
| Patient names | Leading/trailing whitespace trimmed |
| Ghost rows | 1M+ empty Excel rows filtered out (710 real patients kept) |

---

## Dropdown fields (cannot type manually)

These fields only accept values from the predefined lists. No free typing is allowed:

- **Health Partner**: Tanupriya, Abhirami, Khusboo
- **Diet Coach**: Bhakti, Bhumika, Bhuvaneshwari, Dr. Prasanth, Michelle, Radhika, Sahana, Sid, Swetha, Vandna, Vrushali
- **Wellness Coach**: Ankur, Dr. Himval, Manya, Shobika, Shubha, Sid
- **Physio Coach**: Annie, Dr. Bhavan, Dr. Iswarya, Dr. Jiwangi, Nisheshilka, Reema, Ritu, Sahana, Sakshi, Shahil, Sid, shubham
- **CS Agent**: Amisha, Ji
- **Condition Type**: Cholesterol, Diabetes, Weight Management, Hypertension, PCOS, Pre-Diabetic
- **Plan Duration**: 3 Months, 6 Months, 12 Months
- **Call Disposition**: Completed, Partially Completed, No answer, Asked to call later, Not Reachable/Switch Off, Patient did not join the call
- **Status**: Welcome Call Pending, Welcome Call Completed, Month 1-6 Assessment Pending/Completed, Inactive from Month 1-6 Assessment, others, Plan Ended

To add a new value to any dropdown, go to the Coaches tab (for coaches) or ask an Admin.

---

## Free-text fields (manual typing allowed)

These fields accept any text:

- Final/Current Remarks (RM tab)
- Welcome Call Attempt Remarks
- Coach appointment remarks
- CS Remarks
- Current Diet/Wellness/Physio Status notes
- Diet Plan Comments
- Exercise Plan Comments
- Head Coach Comment
- Weekly follow-up Remarks

---

## API Reference (for developers)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/patients` | All patient records |
| GET | `/api/patients/{id}` | Single patient by ID |
| GET | `/api/dropdowns` | All dropdown lists |
| GET | `/api/stats` | Dashboard KPIs |
| GET | `/api/audit` | Full audit trail |
| POST | `/api/patients` | Create new patient |
| PUT | `/api/patients/update` | Update a field on a patient |
| POST | `/api/patients/attempt` | Log a call attempt |
| POST | `/api/patients/weekly` | Log a weekly follow-up entry |
| PUT | `/api/dropdowns` | Add/remove a dropdown value |

---

## Data safety

- **Auto-backups**: Every time someone saves a change, `patients.json` is backed up to `crm_data/backups/` with a timestamp. The last 20 backups are kept.
- **Audit trail**: Every single edit is logged in `audit.json` with the user name, role, patient ID, field changed, old value, new value, and timestamp.
- **No data loss on migration**: All 710 patients migrated with complete history — every welcome call attempt, every monthly assessment, every weekly remark.

## Troubleshooting

**"Failed to connect to server"**
- Make sure `server.py` is running in the terminal
- Check that you're opening the correct URL (http://localhost:8000)

**"Save failed"**
- Check that the server terminal isn't showing errors
- Make sure the `crm_data/` folder has write permissions

**Missing patients after migration**
- The script filters rows where Patient Name is "0", blank, or NaN, and Contact Number has fewer than 7 digits. These are ghost rows from Excel fill-down, not real patients.
- If your Excel has more than 2000 rows of real data, increase `MAX_ROWS` in `migrate.py`

**New coach not appearing in dropdowns**
- Go to the Coaches tab, click "+ Add new coach", enter the name and type. The coach immediately appears in all relevant dropdowns.
