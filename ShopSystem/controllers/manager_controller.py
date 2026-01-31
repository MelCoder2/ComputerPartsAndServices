import re
import database
from datetime import datetime
from PyQt6.QtGui import QTextDocument
from PyQt6.QtPrintSupport import QPrinter


class ManagerController:
    def __init__(self, view):
        self.view = view
        self.current_history_page = 0
        self.history_per_page = 10

    # --- PRODUCT MANAGEMENT ---
    def get_next_product_code(self):
        """Calculates the next available product code"""
        try:
            all_codes = database.get_all_codes()
            if not all_codes:
                return "1001"

            numeric_codes = [int(c) for c in all_codes if str(c).isdigit()]
            return str(max(numeric_codes) + 1) if numeric_codes else "1001"
        except Exception as e:
            print("Next Code Error:", e)
            return "1001"

    def add_product(self, code, name, price, stock, category, details):
        """Adds a new product to inventory"""
        if not name or not price or not stock or not category:
            return False, "Fill all required fields"

        try:
            database.add_product(code, name, float(price), int(stock), category, details)
            return True, f"Product Added with Code: {code}"
        except Exception as e:
            if "already taken" in str(e):
                return False, str(e)
            return False, f"Invalid Input: {e}"

    def restock_product(self, product_id, quantity):
        """Adds stock to an existing product"""
        if quantity <= 0:
            return False, "Quantity must be positive"

        try:
            database.restock_product(product_id, quantity)
            return True, f"Successfully added {quantity} units"
        except Exception as e:
            return False, str(e)

    def delete_product(self, product_id):
        """Soft deletes a product"""
        database.delete_product(product_id)
        return True, "Product deleted"

    def get_all_products(self, category=None, search=None):
        """Returns all active products with optional filtering"""
        return database.get_products(category, search)

    def get_categories(self):
        """Returns all product categories"""
        return database.get_categories()

    # --- CUSTOMER MANAGEMENT ---
    def get_all_customers(self):
        """Returns all registered customers"""
        return database.get_all_customers()

    # --- SERVICE MANAGEMENT ---
    def get_all_services(self):
        """Returns all pending services"""
        return database.get_all_services_joined()

    def mark_service_complete(self, service_id):
        """Marks a service as completed"""
        database.update_service_status(service_id, "Completed")
        return True, "Service marked as completed"

    def delete_service(self, service_id):
        """Deletes a service record"""
        database.delete_service(service_id)
        return True, "Service deleted"

    def get_completed_services(self, page=0):
        """Returns completed services with pagination"""
        offset = page * self.history_per_page
        return database.get_completed_services(self.history_per_page, offset)

    def get_completed_services_count(self):
        """Returns total count of completed services"""
        return database.get_completed_services_count()

    def get_total_history_pages(self):
        """Calculate total pages for history"""
        total = self.get_completed_services_count()
        return max(1, (total + self.history_per_page - 1) // self.history_per_page)

    # --- SALES DATA ---
    def get_all_sales(self):
        """Returns all sales records"""
        return database.get_all_sales()

    # --- STATISTICS ---
    def get_stats(self):
        """Returns dashboard statistics"""
        return database.get_stats()

    # --- REVENUE BREAKDOWN ---
    def get_revenue_breakdown(self):
        """
        Returns revenue breakdown by source
        Returns: list of tuples [(source_name, amount), ...]
        """
        sales_revenue = sum([row[4] for row in self.get_all_sales()])

        # Get completed services revenue from completed_services table
        completed_services = self.get_completed_services()
        services_revenue = sum([row[6] for row in completed_services])

        return [
            ("Product Sales", sales_revenue),
            ("Services", services_revenue),
        ]

    # --- ORDERS BREAKDOWN ---
    def get_orders_breakdown(self):
        """
        Returns orders breakdown by category
        Returns: list of tuples [(category_name, count), ...]
        """
        sales_count = len(self.get_all_sales())
        completed_services = len(self.get_completed_services())
        pending_services = len([s for s in self.get_all_services() if s[4] != "Completed"])

        return [
            ("Product Sales", sales_count),
            ("Completed Services", completed_services),
            ("Pending Services", pending_services),
        ]

    # --- STOCK BREAKDOWN ---
    def get_stock_breakdown(self, low_stock_threshold=5):
        """
        Returns stock breakdown by category
        Returns: dict of {category: {items, total_stock, low_stock}}
        """
        products = self.get_all_products()
        categories = {}

        for product in products:
            pid, code, name, price, stock, cat, details = product
            if cat not in categories:
                categories[cat] = {"items": 0, "total_stock": 0, "low_stock": 0}
            categories[cat]["items"] += 1
            categories[cat]["total_stock"] += stock
            if stock <= low_stock_threshold:
                categories[cat]["low_stock"] += 1

        return categories

    # --- CUSTOMER ANALYSIS ---
    def get_customer_breakdown(self, limit=20):
        """
        Returns customer activity breakdown
        Returns: list of tuples [(customer_name, orders_count, total_spent), ...] sorted by total_spent
        """
        customers = {}

        # From sales
        for sale in self.get_all_sales():
            date, cust, item, qty, total, payment, bank = sale
            if cust not in customers:
                customers[cust] = {"orders": 0, "spent": 0}
            customers[cust]["orders"] += 1
            customers[cust]["spent"] += total

        # From completed services
        completed_services = self.get_completed_services()
        for service in completed_services:
            cust = service[1]  # full_name
            if cust not in customers:
                customers[cust] = {"orders": 0, "spent": 0}
            customers[cust]["orders"] += 1
            customers[cust]["spent"] += service[6]  # price

        # Sort by total spent
        sorted_customers = sorted(customers.items(), key=lambda x: x[1]["spent"], reverse=True)

        # Return all if limit is None, otherwise return top N
        if limit is None:
            return [(cust, data["orders"], data["spent"]) for cust, data in sorted_customers]
        else:
            return [(cust, data["orders"], data["spent"]) for cust, data in sorted_customers[:limit]]

    # --- PDF EXPORT ---
    def export_to_pdf(self, title, headers, data, filename):
        """Generates a PDF report"""
        try:
            date_str = datetime.now().strftime("%B %d, %Y | %I:%M %p")

            html = f"""
            <div style="font-family: 'Segoe UI', Helvetica, sans-serif; padding: 20px; color: #334155;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #009688; margin: 0; padding: 0; font-size: 28px; font-weight: 800;">{title}</h1>
                    <p style="color: #64748b; margin-top: 5px; font-size: 12px;">Generated on: {date_str}</p>
                </div>
                <table width="100%" cellpadding="10" cellspacing="0" style="border-collapse: collapse; border: 1px solid #e2e8f0;">
                    <thead>
                        <tr style="background-color: #f1f5f9; color: #1e293b;">
            """

            for h in headers:
                html += f"<th align='left' style='padding: 12px; font-weight: 700; border-bottom: 2px solid #e2e8f0; font-size: 12px; text-transform: uppercase;'>{h}</th>"

            html += "</tr></thead><tbody>"

            for i, row in enumerate(data):
                bg_color = "#ffffff" if i % 2 == 0 else "#f8fafc"
                html += f"<tr style='background-color: {bg_color};'>"
                for v in row:
                    html += f"<td style='padding: 12px; border-bottom: 1px solid #f1f5f9; color: #334155; font-size: 13px;'>{str(v)}</td>"
                html += "</tr>"

            html += "</tbody></table></div>"

            doc = QTextDocument()
            doc.setHtml(html)
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filename)
            doc.print(printer)

            return True, f"Exported to {filename}"
        except Exception as e:
            return False, str(e)

    # --- LOGOUT ---
    def logout(self):
        """Returns to login screen"""
        # Will be handled by view
        pass