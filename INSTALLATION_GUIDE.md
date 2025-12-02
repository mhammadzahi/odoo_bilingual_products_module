# Bilingual Products Module - Installation & Configuration Guide

## Overview
This module enables Arabic and English translations for product fields in Odoo.

**Translatable fields:**
- Product Name
- Sales Description

**Non-translatable fields (remain same in all languages):**
- External ID, Internal Reference, Barcode, Sales Price, Cost, Weight, Product Type

---

## Installation Steps

### 1. Install the Custom Module

Copy the module to Odoo addons directory:
```bash
# Copy module to Odoo addons path
sudo cp -r /home/mohammad/Desktop/Odoo-tests/bilingual_product /opt/odoo/addons/

# Set proper permissions
sudo chown -R odoo:odoo /opt/odoo/addons/bilingual_product
```

### 2. Update Odoo Apps List

Restart Odoo and update the apps list:
```bash
# Restart Odoo service
sudo systemctl restart odoo

# Or if running manually
sudo su - odoo -s /bin/bash
cd /opt/odoo
./odoo-bin -c /etc/odoo/odoo.conf -u all -d your_database_name --stop-after-init
```

### 3. Install Arabic Language

1. Go to **Settings** → **Translations** → **Load a Translation**
2. Select **Arabic / العربية** (language code: `ar_001` or `ar_SY`, `ar_SA`, etc.)
3. Click **Load**

### 4. Activate the Module

1. Go to **Apps**
2. Remove the "Apps" filter to see all modules
3. Search for "Bilingual Products"
4. Click **Install**

### 5. Enable Translation Mode (Optional but Recommended)

To easily add/edit translations:
1. Go to **Settings** → **Translations**
2. Enable **Developer Mode** first (Settings → Activate the developer mode)
3. Then go to **Settings** → **Technical** → **User Interface** → **Views**
4. Or use URL: `http://your-odoo-url/web?debug=1`

---

## Method 1: Import via Odoo UI

### Step 1: Import English Products
1. Go to **Sales** → **Products**
2. Click the **Favorites** menu (⚙️) → **Import records**
3. Upload your `product_Template.csv`
4. Map the columns correctly:
   - External ID → External ID
   - Name → Name
   - Product Type → Product Type
   - Internal Reference → Internal Reference
   - Barcode → Barcode
   - Sales Price → Sales Price
   - Cost → Cost
   - Weight → Weight
   - Sales Description → Sales Description
5. Click **Import**

### Step 2: Add Arabic Translations
1. Go to any product form
2. Click on the **language selector** next to the Name field (🌐 icon)
3. Select **Arabic**
4. Enter Arabic translation for Name and Description
5. Save

**OR** use bulk import:
1. Export products with External IDs
2. Switch interface language to Arabic
3. Import CSV with Arabic translations (matching External IDs)

---

## Method 2: Import via Python Script (Recommended for Bulk)

### Prerequisites
```bash
# Install Python XML-RPC library (usually pre-installed)
python3 -c "import xmlrpc.client"
```

### Prepare Your CSV Files

**English CSV** (already have): `product_Template.csv`

**Arabic CSV** (example provided): `product_Template_arabic_example.csv`
- Must have same External IDs as English CSV
- Only include Name and Sales Description columns

### Run the Import Script

```bash
cd /home/mohammad/Desktop/Odoo-tests

# Import products with Arabic translations
python3 import_bilingual_products.py \
    --csv product_Template.csv \
    --arabic-csv product_Template_arabic_example.csv \
    --url http://localhost:8069 \
    --db your_database_name \
    --user admin \
    --password your_password \
    --lang ar_001
```

**Parameters:**
- `--csv`: Path to English CSV file
- `--arabic-csv`: Path to Arabic CSV file (optional)
- `--url`: Your Odoo URL (default: http://localhost:8069)
- `--db`: Database name
- `--user`: Odoo username (usually admin)
- `--password`: User password
- `--lang`: Arabic language code (ar_001, ar_SY, ar_SA, etc.)

---

## Method 3: Direct SQL (Advanced - Use with Caution)

If you have direct database access:

```bash
# Connect to PostgreSQL
sudo -u postgres psql your_database_name

# Check if Arabic is installed
SELECT code, name FROM res_lang WHERE code LIKE 'ar%';

# If not installed, you need to install via UI first
```

After importing via UI or script, translations are stored in `ir_translation` table.

---

## Verification

### Check if Translation Works:
1. Switch user language to Arabic:
   - Click on your username → **Preferences**
   - Change **Language** to **العربية / Arabic**
   - Save
2. Go to **Products** and verify Arabic names appear

### Test Both Languages:
1. Create a product manually
2. Set English name: "Test Product"
3. Click language icon (🌐) next to Name field
4. Select Arabic and enter: "منتج تجريبي"
5. Switch interface language and verify both versions appear

---

## Switching Between Languages

### For Users:
- Each user can set their preferred language in Preferences
- Products will show in their language automatically

### For Product Forms:
- Use the 🌐 icon next to translatable fields to edit translations
- You can see/edit all languages from one place

---

## Updating Existing Products

If products already exist in your database:

```bash
# Re-import with same External IDs - they will update
python3 import_bilingual_products.py \
    --csv product_Template.csv \
    --arabic-csv product_Template_arabic_example.csv \
    --url http://localhost:8069 \
    --db your_database_name \
    --user admin \
    --password your_password
```

---

## Troubleshooting

### Module not appearing in Apps list:
```bash
# Check module is in correct path
ls -la /opt/odoo/addons/bilingual_product

# Update apps list
sudo su - odoo -s /bin/bash
cd /opt/odoo
./odoo-bin -c /etc/odoo/odoo.conf -u all -d your_db --stop-after-init
```

### Arabic language not available:
- Install via Settings → Translations → Load a Translation
- Make sure Arabic locale is installed on your system:
  ```bash
  locale -a | grep ar
  ```

### Translations not showing:
1. Verify Arabic language is installed (Settings → Translations → Languages)
2. Check if fields have `translate=True` in the model
3. Clear browser cache
4. Restart Odoo: `sudo systemctl restart odoo`

### Import script errors:
- Verify Odoo is running: `sudo systemctl status odoo`
- Check firewall allows connection to port 8069
- Verify credentials are correct
- Check if XML-RPC is enabled in `odoo.conf` (it's enabled by default)

---

## Configuration File Reference

If you need to modify `/etc/odoo/odoo.conf`:

```ini
[options]
addons_path = /opt/odoo/addons,/opt/odoo/custom_addons
admin_passwd = your_master_password
db_host = localhost
db_port = 5432
db_user = odoo
db_password = your_db_password
xmlrpc_port = 8069
```

---

## Additional Tips

### Making More Fields Translatable

Edit `/opt/odoo/addons/bilingual_product/models/product_template.py`:

```python
# Example: Make internal notes translatable
description = fields.Text(
    'Description',
    translate=True
)
```

Then upgrade the module:
```bash
sudo su - odoo -s /bin/bash
./odoo-bin -c /etc/odoo/odoo.conf -u bilingual_product -d your_db --stop-after-init
```

### Export Products with Translations

1. Switch to Arabic language
2. Go to Products
3. Export products → Arabic names will be in the export
4. Switch to English and export again → English names in export

### Using Translation Terms View

1. Enable Developer Mode
2. Go to Settings → Translations → Translated Terms
3. Filter by Model = "product.template"
4. Edit translations in bulk

---

## Support

For Odoo version-specific issues:
- Odoo 14/15/16/17: This module should work with minor adjustments
- Check Odoo documentation: https://www.odoo.com/documentation/

For module issues:
- Check Odoo logs: `sudo tail -f /var/log/odoo/odoo-server.log`
- Enable debug mode for detailed errors
