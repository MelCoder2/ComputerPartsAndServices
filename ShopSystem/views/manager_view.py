import re
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QTabWidget,
    QFrame, QLineEdit, QGridLayout, QAbstractItemView, QFileDialog,
    QComboBox, QTextEdit, QDialog, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QCursor
from controllers.manager_controller import ManagerController


class RestockDialog(QDialog):
    """Dialog to restock a product"""

    def __init__(self, parent, product_code, product_name, current_stock):
        super().__init__(parent)
        self.setWindowTitle("Restock Product")
        self.setFixedSize(450, 350)
        self.setModal(True)

        # Ensure dialog appears on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        # Set solid background
        self.setStyleSheet("""
            QDialog { 
                background-color: #f8fafc;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel(f"Restock: {product_name}")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px; 
                font-weight: bold; 
                color: #0f172a;
                background: transparent;
                border: none;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Info container
        info_container = QWidget()
        info_container.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
        """)
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(15)
        info_layout.setContentsMargins(25, 25, 25, 25)

        # Current stock
        current_label = QLabel(f"Current Stock: {current_stock} units")
        current_label.setStyleSheet("""
            QLabel {
                font-size: 14px; 
                color: #64748b; 
                background: transparent; 
                border: none;
            }
        """)
        info_layout.addWidget(current_label)

        # Add quantity section
        qty_label = QLabel("Add Quantity:")
        qty_label.setStyleSheet("""
            QLabel {
                font-weight: 700;
                color: #1e293b;
                font-size: 14px;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px 0px 6px 0px;
            }
        """)
        info_layout.addWidget(qty_label)

        # QSpinBox with MINIMAL styling to let Qt handle the arrows
        self.qty_input = QSpinBox()
        self.qty_input.setMinimum(1)
        self.qty_input.setMaximum(10000)
        self.qty_input.setValue(10)
        self.qty_input.setFixedHeight(48)

        # KEY: Use UpDownArrows button symbols
        self.qty_input.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)

        # SIMPLER stylesheet - let Qt draw the arrows naturally
        self.qty_input.setStyleSheet("""
            QSpinBox {
                background-color: #ffffff;
                border: 2px solid #cbd5e1;
                border-radius: 6px;
                padding-left: 12px;
                color: #334155;
                font-size: 16px;
                font-weight: bold;
            }
            QSpinBox:focus {
                border: 2px solid #009688;
            }
        """)

        info_layout.addWidget(self.qty_input)

        main_layout.addWidget(info_container)
        main_layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedHeight(48)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background: white;
                border: 1px solid #cbd5e1;
                color: #475569;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background: #f1f5f9; }
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_confirm = QPushButton("Confirm Restock")
        btn_confirm.setFixedHeight(48)
        btn_confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_confirm.setStyleSheet("""
            QPushButton {
                background: #009688;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background: #00796b; }
        """)
        btn_confirm.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_confirm)
        main_layout.addLayout(btn_layout)

    def get_quantity(self):
        return self.qty_input.value()


class StatDetailDialog(QDialog):
    """Dialog to show detailed information for each stat card"""

    def __init__(self, parent, title, content_widget):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header = QLabel(title)
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e293b;")
        layout.addWidget(header)

        # Content
        layout.addWidget(content_widget)

        # Close button
        btn_close = QPushButton("Close")
        btn_close.setFixedWidth(120)
        btn_close.setFixedHeight(40)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #009688;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #00796b;
            }
        """)
        btn_close.clicked.connect(self.accept)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)


class ManagerView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = ManagerController(self)
        self.setWindowTitle("Manager Window")
        self.resize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("QWidget#centralWidget { background-color: #f8fafc; }")
        central.setObjectName("centralWidget")
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # HEADER
        top = QHBoxLayout()
        tl = QVBoxLayout()
        t = QLabel("Manager Dashboard")
        t.setStyleSheet("font-size: 30px; font-weight: bold; color: #1e293b; background: none;")
        s = QLabel("Manage inventory & services.")
        s.setStyleSheet("color: #64748b; font-size: 20px; background: none;")
        tl.addWidget(t)
        tl.addWidget(s)

        self.btn_profile = QPushButton(" 👤 Store Manager")
        self.btn_profile.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #334155;
                font-size: 15px;
                font-weight: bold;
            }
        """)

        # RED SIGN OUT BUTTON
        logout = QPushButton("➥🚪 Sign Out")
        logout.setFixedWidth(140)
        logout.setFixedHeight(40)
        logout.setStyleSheet("""
            QPushButton {
                background: #fee2e2;
                border: 1px solid #fecaca;
                border-radius: 6px;
                padding: 8px;
                color: #b91c1c;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #fca5a5;
                color: #7f1d1d;
                border-color: #fca5a5;
            }
        """)
        logout.clicked.connect(self.on_logout_clicked)

        top.addLayout(tl)
        top.addStretch()
        top.addWidget(self.btn_profile)
        top.addWidget(logout)
        main_layout.addLayout(top)

        # CLICKABLE STATS
        stats = QHBoxLayout()
        stats.setSpacing(20)

        self.c1, self.l1 = self.stat_card("💰 Total Revenue", "#10b981", self.show_revenue_details)
        self.c2, self.l2 = self.stat_card("🧾 Total Orders", "#3b82f6", self.show_orders_details)
        self.c3, self.l3 = self.stat_card("📦 Stock Count", "#f59e0b", self.show_stock_details)
        self.c4, self.l4 = self.stat_card("👥 Customers", "#8b5cf6", self.show_customers_details)

        stats.addWidget(self.c1)
        stats.addWidget(self.c2)
        stats.addWidget(self.c3)
        stats.addWidget(self.c4)
        main_layout.addLayout(stats)

        # TABS
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                background: white;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #e2e8f0;
                padding: 10px 20px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                color: #64748b;
            }
            QTabBar::tab:selected {
                background: white;
                color: #0f172a;
                border-bottom: none;
            }
            QTabWidget > QWidget {
                background-color: #f8fafc;
            }
        """)
        main_layout.addWidget(self.tabs)

        self.init_inventory_tab()
        self.init_services_tab()
        self.init_history_tab()
        self.init_sales_tab()

        QTimer.singleShot(100, self.refresh_all)

    def stat_card(self, title, color, click_handler):
        """Create a clickable stat card"""
        f = QFrame()
        f.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #cbd5e1;
                border-left: 5px solid {color};
            }}
            QFrame:hover {{
                background-color: #f8fafc;
                border: 1px solid #94a3b8;
                border-left: 5px solid {color};
            }}
        """)
        f.setFixedHeight(100)
        f.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Make the frame clickable
        f.mousePressEvent = lambda event: click_handler()

        l = QVBoxLayout(f)
        l.setContentsMargins(20, 15, 20, 15)

        t = QLabel(title)
        t.setStyleSheet("color: #64748b; font-weight: bold; border:none; background:transparent;")

        v = QLabel("0")
        v.setStyleSheet("color: #1e293b; font-size: 28px; font-weight: 900; border:none; background:transparent;")

        l.addWidget(t)
        l.addWidget(v)

        return f, v

    def show_revenue_details(self):
        """Show detailed revenue breakdown"""
        content = QWidget()
        layout = QVBoxLayout(content)

        # Revenue summary
        summary = QLabel("Revenue Breakdown")
        summary.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(summary)

        # Create table for revenue details
        table = QTableWidget(0, 3)
        table.setHorizontalHeaderLabels(["Source", "Amount", "Percentage"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px;
                border: none;
                font-weight: bold;
                color: #1e293b;
            }
        """)

        # Get revenue data
        sales_revenue = sum([row[4] for row in self.controller.get_all_sales()])
        # Get completed services revenue from completed_services table
        completed_services = self.controller.get_completed_services()
        services_revenue = sum([row[6] for row in completed_services])  # row[6] is price in completed_services
        total_revenue = sales_revenue + services_revenue

        revenue_data = [
            ("Product Sales", sales_revenue),
            ("Services", services_revenue),
        ]

        for source, amount in revenue_data:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(source))
            table.setItem(row, 1, QTableWidgetItem(f"₱{amount:,.2f}"))
            percentage = (amount / total_revenue * 100) if total_revenue > 0 else 0
            table.setItem(row, 2, QTableWidgetItem(f"{percentage:.1f}%"))

        layout.addWidget(table)

        # Total
        total_label = QLabel(f"Total Revenue: ₱{total_revenue:,.2f}")
        total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #10b981; margin-top: 20px;")
        layout.addWidget(total_label)

        dialog = StatDetailDialog(self, "💰 Revenue Details", content)
        dialog.exec()

    def show_orders_details(self):
        """Show detailed orders breakdown"""
        content = QWidget()
        layout = QVBoxLayout(content)

        # Orders summary
        summary = QLabel("Orders Overview")
        summary.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(summary)

        # Create table
        table = QTableWidget(0, 3)
        table.setHorizontalHeaderLabels(["Category", "Count", "Percentage"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px;
                border: none;
                font-weight: bold;
                color: #1e293b;
            }
        """)

        # Get orders data
        sales_count = len(self.controller.get_all_sales())
        completed_services = len([s for s in self.controller.get_completed_services()])
        pending_services = len([s for s in self.controller.get_all_services() if s[4] != "Completed"])
        total_orders = sales_count + completed_services + pending_services

        orders_data = [
            ("Product Sales", sales_count),
            ("Completed Services", completed_services),
            ("Pending Services", pending_services),
        ]

        for category, count in orders_data:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(category))
            table.setItem(row, 1, QTableWidgetItem(str(count)))
            percentage = (count / total_orders * 100) if total_orders > 0 else 0
            table.setItem(row, 2, QTableWidgetItem(f"{percentage:.1f}%"))

        layout.addWidget(table)

        # Total
        total_label = QLabel(f"Total Orders: {total_orders}")
        total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3b82f6; margin-top: 20px;")
        layout.addWidget(total_label)

        dialog = StatDetailDialog(self, "🧾 Orders Details", content)
        dialog.exec()

    def show_stock_details(self):
        """Show detailed stock information with individual items"""
        content = QWidget()
        layout = QVBoxLayout(content)

        # Stock summary
        summary = QLabel("Inventory Status - All Products")
        summary.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(summary)

        # Search bar
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Search products...")
        search_input.setFixedHeight(40)
        search_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #009688;
                outline: none;
            }
        """)
        search_layout.addWidget(search_input)
        layout.addLayout(search_layout)

        # Create table for individual products
        table = QTableWidget(0, 4)
        table.setHorizontalHeaderLabels(["Category", "Product Name", "Code", "Stock"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px;
                border: none;
                font-weight: bold;
                color: #1e293b;
            }
        """)

        # Get all products
        products = self.controller.get_all_products()
        all_product_data = [(p[5], p[2], p[1], p[4]) for p in products]  # category, name, code, stock

        def populate_table(search_text=""):
            """Populate table with optional search filter"""
            table.setRowCount(0)
            filtered_data = [
                (cat, name, code, stock) for cat, name, code, stock in all_product_data
                if
                search_text.lower() in name.lower() or search_text.lower() in code.lower() or search_text.lower() in cat.lower()
            ]

            # Sort by category first, then by name
            filtered_data.sort(key=lambda x: (x[0], x[1]))

            for cat, name, code, stock in filtered_data:
                row = table.rowCount()
                table.insertRow(row)

                cat_item = QTableWidgetItem(cat)
                cat_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                table.setItem(row, 0, cat_item)

                table.setItem(row, 1, QTableWidgetItem(name))
                table.setItem(row, 2, QTableWidgetItem(code))

                stock_item = QTableWidgetItem(str(stock))
                if stock <= 5:  # Low stock threshold
                    stock_item.setForeground(QColor("#ef4444"))
                    stock_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                else:
                    stock_item.setForeground(QColor("#10b981"))
                table.setItem(row, 3, stock_item)

        # Connect search input to table filtering
        search_input.textChanged.connect(populate_table)

        # Initial population
        populate_table()

        layout.addWidget(table)

        # Total
        total_stock = sum([p[4] for p in products])
        low_stock_count = len([p for p in products if p[4] <= 5])
        total_label = QLabel(f"Total Stock Units: {total_stock} | Low Stock Items: {low_stock_count}")
        total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #f59e0b; margin-top: 20px;")
        layout.addWidget(total_label)

        dialog = StatDetailDialog(self, "📦 Stock Details", content)
        dialog.exec()

    def show_customers_details(self):
        """Show detailed customer information with search"""
        content = QWidget()
        layout = QVBoxLayout(content)

        # Customer summary
        summary = QLabel("Customer Activity")
        summary.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(summary)

        # Search bar
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Search customers...")
        search_input.setFixedHeight(40)
        search_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #009688;
                outline: none;
            }
        """)
        search_layout.addWidget(search_input)
        layout.addLayout(search_layout)

        # Create table
        table = QTableWidget(0, 3)
        table.setHorizontalHeaderLabels(["Customer", "Total Orders", "Total Spent"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px;
                border: none;
                font-weight: bold;
                color: #1e293b;
            }
        """)

        # Get ALL registered customers first
        all_customers = self.controller.get_all_customers()
        customers = {}

        # Initialize all customers with 0 orders and 0 spent
        for customer_data in all_customers:
            full_name = customer_data[0]  # full_name from database
            customers[full_name] = {"orders": 0, "spent": 0}

        # From sales
        for sale in self.controller.get_all_sales():
            date, cust, item, qty, total, payment, bank = sale
            if cust not in customers:
                customers[cust] = {"orders": 0, "spent": 0}
            customers[cust]["orders"] += 1
            customers[cust]["spent"] += total

        # From completed services
        for service in self.controller.get_completed_services():
            cust = service[1]  # full_name is at index 1 in completed_services
            if cust not in customers:
                customers[cust] = {"orders": 0, "spent": 0}
            customers[cust]["orders"] += 1
            customers[cust]["spent"] += service[6]  # price is at index 6

        # Store all customers data for filtering
        all_customer_data = sorted(customers.items(), key=lambda x: (-x[1]["spent"], x[0]))

        def populate_table(search_text=""):
            """Populate table with optional search filter"""
            table.setRowCount(0)
            filtered_data = [
                (customer, data) for customer, data in all_customer_data
                if search_text.lower() in customer.lower()
            ]

            for customer, data in filtered_data:
                row = table.rowCount()
                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem(customer))
                table.setItem(row, 1, QTableWidgetItem(str(data["orders"])))
                table.setItem(row, 2, QTableWidgetItem(f"₱{data['spent']:,.2f}"))

        # Connect search input to table filtering
        search_input.textChanged.connect(populate_table)

        # Initial population
        populate_table()

        layout.addWidget(table)

        # Total
        total_label = QLabel(f"Total Unique Customers: {len(customers)}")
        total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #8b5cf6; margin-top: 20px;")
        layout.addWidget(total_label)

        dialog = StatDetailDialog(self, "👥 Customer Details", content)
        dialog.exec()

    def on_logout_clicked(self):
        from views.login_view import LoginView
        self.login_window = LoginView()
        self.login_window.show()
        self.close()

    # === INVENTORY TAB ===
    def init_inventory_tab(self):
        tab = QWidget()
        l = QVBoxLayout(tab)
        l.setContentsMargins(30, 30, 30, 30)
        l.setSpacing(20)

        c = QFrame()
        c.setStyleSheet("QFrame { background: white; border: 1px solid #cbd5e1; border-radius: 12px; }")
        cl = QVBoxLayout(c)
        cl.setContentsMargins(20, 20, 20, 20)

        g = QGridLayout()
        g.setVerticalSpacing(15)
        g.setHorizontalSpacing(20)

        self.ic = QLineEdit()
        self.ic.setPlaceholderText("Auto")
        self.ic.setReadOnly(True)
        self.ic.setStyleSheet("""
            QLineEdit {
                background-color: #e0f2f1;
                color: #00796b;
                border: 0px;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 0px;
                outline: none;
            }
        """)

        self.inm = QLineEdit(placeholderText="Name")
        self.ip = QLineEdit(placeholderText="0.00")

        # CHANGED: Stock field is now a QSpinBox instead of QLineEdit
        self.is_ = QSpinBox()
        self.is_.setMinimum(1)
        self.is_.setMaximum(10000)
        self.is_.setValue(1)
        self.is_.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.is_.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding-left: 10px;
                color: #334155;
                font-size: 14px;
            }
            QSpinBox:focus {
                background-color: white;
                border: 2px solid #009688;
                outline: none;
            }
        """)

        self.icat = QComboBox()
        self.icat.addItems(
            ["CPU", "GPU", "RAM", "Storage", "Motherboard", "PSU", "Case", "Cooling", "Peripherals", "Other"])
        self.icat.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
                padding-right: 30px;
                color: #334155;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 1px solid #cbd5e1;
            }
            QComboBox:focus {
                background-color: white;
                border: 2px solid #009688;
                outline: none;
            }
        """)

        input_style = """
            QLineEdit {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
                color: #334155;
                font-size: 14px;
            }
            QLineEdit:focus {
                background-color: white;
                border: 2px solid #009688;
                outline: none;
            }
        """

        # Apply styles to Name and Price fields only (not Stock anymore)
        for w in [self.inm, self.ip]:
            w.setFixedHeight(45)
            w.setStyleSheet(input_style)

        self.icat.setFixedHeight(45)
        self.icat.setFixedWidth(200)
        self.ic.setFixedHeight(45)
        self.is_.setFixedHeight(45)  # Set height for spinbox

        lbl_style = "background-color: transparent; font-weight: bold; color: #1e293b; border: none;"

        g.addWidget(QLabel("Code:", styleSheet=lbl_style), 0, 0)
        g.addWidget(self.ic, 1, 0)
        g.addWidget(QLabel("Name:", styleSheet=lbl_style), 0, 1)
        g.addWidget(self.inm, 1, 1)
        g.addWidget(QLabel("Price:", styleSheet=lbl_style), 0, 2)
        g.addWidget(self.ip, 1, 2)
        g.addWidget(QLabel("Stock:", styleSheet=lbl_style), 0, 3)
        g.addWidget(self.is_, 1, 3)
        g.addWidget(QLabel("Category:", styleSheet=lbl_style), 0, 4)
        g.addWidget(self.icat, 1, 4)

        btn = QPushButton("➕ Add Product", cursor=Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(40)
        btn.setFixedWidth(150)
        btn.setStyleSheet(
            "background-color: #009688; color: white; border-radius: 6px; font-weight: bold; font-size: 14px; border: none;")
        btn.clicked.connect(self.on_add_product_clicked)
        g.addWidget(btn, 1, 5)

        cl.addLayout(g)
        l.addWidget(c)

        # FILTER BAR
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(15)
        filter_bar.addWidget(
            QLabel("Filter:", styleSheet="font-weight: bold; color: #334155; font-size: 14px; border: none;"))

        self.filter_cat = QComboBox()
        self.filter_cat.addItem("All Categories")
        self.filter_cat.setFixedHeight(45)
        self.filter_cat.setStyleSheet("""
            QComboBox {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
                padding-right: 30px;
                min-width: 180px;
                font-size: 14px;
                color: #334155;
            }
            QComboBox:hover {
                border: 1px solid #cbd5e1;
            }
            QComboBox:focus {
                border: 2px solid #009688;
                outline: none;
            }
        """)
        self.filter_cat.currentTextChanged.connect(self.refresh_inventory)
        filter_bar.addWidget(self.filter_cat)

        self.filter_search = QLineEdit()
        self.filter_search.setPlaceholderText("🔍 Search products...")
        self.filter_search.setFixedWidth(350)
        self.filter_search.setFixedHeight(45)
        self.filter_search.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #009688;
                outline: none;
            }
        """)
        self.filter_search.textChanged.connect(self.refresh_inventory)
        filter_bar.addWidget(self.filter_search)

        filter_bar.addStretch()
        l.addLayout(filter_bar)

        self.inv_t = QTableWidget(0, 6)
        self.inv_t.setHorizontalHeaderLabels(["CODE", "NAME", "PRICE", "STOCK", "CATEGORY", "ACTION"])
        self.inv_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.inv_t.setAlternatingRowColors(True)
        self.inv_t.verticalHeader().setVisible(False)
        self.inv_t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.inv_t.setShowGrid(False)
        self.inv_t.setFrameShape(QFrame.Shape.NoFrame)
        self.inv_t.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.inv_t.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.inv_t.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                outline: none;
                gridline-color: transparent;
                background-color: white;
            }
            QTableWidget::item {
                border: none;
                outline: none;
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                font-weight: bold;
                color: #1e293b;
            }
            QLabel {
                border: none;
                outline: none;
            }
        """)

        l.addWidget(self.inv_t)
        self.tabs.addTab(tab, " 📦 Inventory ")

    # ========================================
    # ALSO UPDATE on_add_product_clicked METHOD
    # ========================================
    def on_add_product_clicked(self):
        next_code = self.controller.get_next_product_code()
        if self.ic.text() and self.ic.text() != "Auto":
            next_code = self.ic.text()

        # CHANGED: Use .value() instead of .text() for spinbox
        success, msg = self.controller.add_product(
            next_code,
            self.inm.text(),
            self.ip.text(),
            str(self.is_.value()),  # Convert spinbox value to string
            self.icat.currentText(),
            ""
        )

        if success:
            self.inm.clear()
            self.ip.clear()
            self.is_.setValue(1)  # Reset spinbox to 1
            self.refresh_all()
            QMessageBox.information(self, "Success", msg)
        else:
            QMessageBox.warning(self, "Error", msg)

    def init_services_tab(self):
        tab = QWidget()
        l = QVBoxLayout(tab)
        l.setContentsMargins(30, 30, 30, 30)

        self.srv_t = QTableWidget(0, 7)
        self.srv_t.setHorizontalHeaderLabels(["CUSTOMER", "SERVICE TYPE", "DETAILS", "TOTAL", "STATUS", "", ""])
        self.srv_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.srv_t.setAlternatingRowColors(True)
        self.srv_t.verticalHeader().setVisible(False)
        self.srv_t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.srv_t.setWordWrap(True)
        self.srv_t.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.srv_t.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.srv_t.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.srv_t.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                outline: none;
                gridline-color: transparent;
                background-color: white;
            }
            QTableWidget::item {
                border: none;
                outline: none;
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                font-weight: bold;
                color: #1e293b;
            }
        """)

        l.addWidget(self.srv_t)

        bl = QHBoxLayout()
        br = QPushButton("🔁 Refresh")
        br.setFixedWidth(150)
        br.setFixedHeight(40)
        br.setStyleSheet("""
            QPushButton {
                background: white;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                color: #475569;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #f1f5f9;
            }
        """)
        br.clicked.connect(self.refresh_all)
        bl.addStretch()
        bl.addWidget(br)
        l.addLayout(bl)

        self.tabs.addTab(tab, " 🛠️ Pending Services ")

    def init_history_tab(self):
        tab = QWidget()
        l = QVBoxLayout(tab)
        l.setContentsMargins(30, 30, 30, 30)

        self.hist_t = QTableWidget(0, 6)
        self.hist_t.setHorizontalHeaderLabels(["COMPLETED", "CUSTOMER", "SERVICE", "STATUS", "TOTAL", "STARTED"])
        self.hist_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.hist_t.setAlternatingRowColors(True)
        self.hist_t.verticalHeader().setVisible(False)
        self.hist_t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.hist_t.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.hist_t.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.hist_t.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                outline: none;
                gridline-color: transparent;
                background-color: white;
            }
            QTableWidget::item {
                border: none;
                outline: none;
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                font-weight: bold;
                color: #1e293b;
            }
        """)

        l.addWidget(self.hist_t)

        # PAGINATION
        page_layout = QHBoxLayout()
        self.lbl_page = QLabel("Page 1 of 1")
        self.lbl_page.setStyleSheet("font-weight: bold; color: #334155; border: none;")

        self.btn_prev = QPushButton("◀ Previous")
        self.btn_prev.setFixedWidth(120)
        self.btn_prev.setFixedHeight(40)
        self.btn_prev.setStyleSheet("""
            QPushButton {
                background: white;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                color: #475569;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #f1f5f9;
            }
            QPushButton:disabled {
                background: #f8fafc;
                color: #cbd5e1;
            }
        """)
        self.btn_prev.clicked.connect(self.prev_page)

        self.btn_next = QPushButton("Next ▶")
        self.btn_next.setFixedWidth(120)
        self.btn_next.setFixedHeight(40)
        self.btn_next.setStyleSheet("""
            QPushButton {
                background: white;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                color: #475569;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #f1f5f9;
            }
            QPushButton:disabled {
                background: #f8fafc;
                color: #cbd5e1;
            }
        """)
        self.btn_next.clicked.connect(self.next_page)

        bp = QPushButton("📄 Export PDF")
        bp.setFixedWidth(150)
        bp.setFixedHeight(40)
        bp.setStyleSheet("""
            QPushButton {
                background: #009688;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #00796b;
            }
        """)
        bp.clicked.connect(self.on_export_history_clicked)

        page_layout.addWidget(self.btn_prev)
        page_layout.addWidget(self.lbl_page)
        page_layout.addWidget(self.btn_next)
        page_layout.addStretch()
        page_layout.addWidget(bp)
        l.addLayout(page_layout)

        self.tabs.addTab(tab, " 📜 Completed Services ")

    def init_sales_tab(self):
        tab = QWidget()
        l = QVBoxLayout(tab)
        l.setContentsMargins(30, 30, 30, 30)

        self.sal_t = QTableWidget(0, 7)
        self.sal_t.setHorizontalHeaderLabels(["DATE", "CUSTOMER", "ITEM", "QTY", "TOTAL", "PAYMENT", "BANK"])
        self.sal_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sal_t.setAlternatingRowColors(True)
        self.sal_t.verticalHeader().setVisible(False)
        self.sal_t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.sal_t.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.sal_t.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sal_t.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                outline: none;
                gridline-color: transparent;
                background-color: white;
            }
            QTableWidget::item {
                border: none;
                outline: none;
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                font-weight: bold;
                color: #1e293b;
            }
        """)

        l.addWidget(self.sal_t)

        bl = QHBoxLayout()
        bp = QPushButton("📄 Export PDF")
        bp.setFixedWidth(150)
        bp.setFixedHeight(40)
        bp.setStyleSheet("""
            QPushButton {
                background: #009688;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #00796b;
            }
        """)
        bp.clicked.connect(self.on_export_sales_clicked)
        bl.addStretch()
        bl.addWidget(bp)
        l.addLayout(bl)

        self.tabs.addTab(tab, " 💰 Sales Report ")

    def prev_page(self):
        if self.controller.current_history_page > 0:
            self.controller.current_history_page -= 1
            self.refresh_history()

    def next_page(self):
        total_pages = self.controller.get_total_history_pages()
        if self.controller.current_history_page < total_pages - 1:
            self.controller.current_history_page += 1
            self.refresh_history()

    def on_restock_product_clicked(self, pid):
        """Handle restock button click"""
        # Get product details
        products = self.controller.get_all_products()
        product = next((p for p in products if p[0] == pid), None)

        if not product:
            QMessageBox.warning(self, "Error", "Product not found")
            return

        _, code, name, price, current_stock, cat, details = product

        # Show restock dialog
        dialog = RestockDialog(self, code, name, current_stock)

        if dialog.exec():
            qty = dialog.get_quantity()
            success, msg = self.controller.restock_product(pid, qty)

            if success:
                self.refresh_all()
                QMessageBox.information(self, "Success", f"Added {qty} units to {name}")
            else:
                QMessageBox.warning(self, "Error", msg)

    def on_delete_product_clicked(self, pid):
        if QMessageBox.question(self, "Confirm", "Delete this product?") == QMessageBox.StandardButton.Yes:
            self.controller.delete_product(pid)
            self.refresh_all()

    def on_mark_complete_clicked(self, sid):
        if QMessageBox.question(self, "Confirm", "Mark as Completed?") == QMessageBox.StandardButton.Yes:
            self.controller.mark_service_complete(sid)
            self.refresh_all()

    def on_delete_service_clicked(self, sid):
        if QMessageBox.question(self, "Confirm", "Delete this record?") == QMessageBox.StandardButton.Yes:
            self.controller.delete_service(sid)
            self.refresh_all()

    def on_export_sales_clicked(self):
        try:
            headers = ["Date", "Customer", "Item", "Qty", "Total", "Payment", "Bank"]
            data = self.controller.get_all_sales()
            fn, _ = QFileDialog.getSaveFileName(self, "Export", "Sales_Report.pdf", "PDF (*.pdf)")
            if fn:
                success, msg = self.controller.export_to_pdf("Sales Report", headers, data, fn)
                if success:
                    QMessageBox.information(self, "Saved", msg)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def on_export_history_clicked(self):
        try:
            raw_data = self.controller.get_completed_services()
            formatted_data = [[row[5], row[1], row[2], "Completed", f"₱{row[6]:,.2f}", row[4]] for row in raw_data]
            headers = ["Date Completed", "Customer", "Service", "Status", "Total", "Date Started"]
            fn, _ = QFileDialog.getSaveFileName(self, "Export", "History.pdf", "PDF (*.pdf)")
            if fn:
                success, msg = self.controller.export_to_pdf("Service History", headers, formatted_data, fn)
                if success:
                    QMessageBox.information(self, "Saved", msg)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def refresh_all(self):
        self.refresh_stats()
        self.refresh_inventory()
        self.refresh_services()
        self.refresh_history()
        self.refresh_sales()

        categories = self.controller.get_categories()
        current_text = self.filter_cat.currentText()
        self.filter_cat.blockSignals(True)
        self.filter_cat.clear()
        self.filter_cat.addItem("All Categories")
        self.filter_cat.addItems(categories)
        if current_text in categories or current_text == "All Categories":
            self.filter_cat.setCurrentText(current_text)
        self.filter_cat.blockSignals(False)

    def refresh_stats(self):
        try:
            rev, orders, stk, custs = self.controller.get_stats()
            self.l1.setText(f"₱{rev:,.2f}")
            self.l2.setText(str(orders))
            self.l3.setText(str(stk))
            self.l4.setText(str(custs))
            self.ic.setText(self.controller.get_next_product_code())
        except Exception as e:
            print("Stats Error:", e)

    def refresh_inventory(self):
        try:
            category = None if self.filter_cat.currentText() == "All Categories" else self.filter_cat.currentText()
            search = self.filter_search.text() if self.filter_search.text() else None
            products = self.controller.get_all_products(category, search)
            self.inv_t.setRowCount(0)

            for row_data in products:
                pid, code, name, price, stock, cat, details = row_data
                r = self.inv_t.rowCount()
                self.inv_t.insertRow(r)
                self.inv_t.setRowHeight(r, 70)

                def make_item(text):
                    it = QTableWidgetItem(str(text))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    return it

                self.inv_t.setItem(r, 0, make_item(code))
                self.inv_t.setItem(r, 1, make_item(name))
                self.inv_t.setItem(r, 2, make_item(f"₱{price:,.2f}"))

                st = make_item(str(stock))
                st.setForeground(QColor("#ef4444") if stock == 0 else QColor("#10b981"))
                st.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                self.inv_t.setItem(r, 3, st)

                self.inv_t.setItem(r, 4, make_item(cat))

                # ACTION BUTTONS: Restock + Delete
                action_widget = QWidget()
                action_widget.setStyleSheet("background: transparent;")
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(5, 0, 5, 0)
                action_layout.setSpacing(5)
                action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Restock button
                btn_restock = QPushButton("Restock")
                btn_restock.setFixedSize(110, 34)
                btn_restock.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_restock.setStyleSheet("""
                    QPushButton {
                        background: #d1fae5;
                        color: #065f46;
                        border: 1px solid #a7f3d0;
                        border-radius: 6px;
                        font-weight: bold;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background: #a7f3d0;
                        color: #064e3b;
                    }
                """)
                btn_restock.clicked.connect(lambda _, x=pid: self.on_restock_product_clicked(x))
                action_layout.addWidget(btn_restock)

                # Delete button
                bd = QPushButton("Delete")
                bd.setFixedSize(110, 34)
                bd.setCursor(Qt.CursorShape.PointingHandCursor)
                bd.setStyleSheet("""
                    QPushButton {
                        background: #fee2e2;
                        color: #b91c1c;
                        border: 1px solid #fecaca;
                        border-radius: 6px;
                        font-weight: bold;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background: #fca5a5;
                        color: #7f1d1d;
                    }
                """)
                bd.clicked.connect(lambda _, x=pid: self.on_delete_product_clicked(x))
                action_layout.addWidget(bd)

                self.inv_t.setCellWidget(r, 5, action_widget)

        except Exception as e:
            print(f"Inventory Error: {e}")
            import traceback
            traceback.print_exc()

    def refresh_services(self):
        try:
            services = self.controller.get_all_services()
            self.srv_t.setRowCount(0)

            for row_data in services:
                sid, cust, svc_type, raw_desc, status, price = row_data
                if status == "Completed":
                    continue

                r = self.srv_t.rowCount()
                self.srv_t.insertRow(r)

                def make_item(text):
                    it = QTableWidgetItem(str(text))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    return it

                self.srv_t.setItem(r, 0, make_item(cust))
                self.srv_t.setItem(r, 1, make_item(svc_type))

                details_item = QTableWidgetItem(raw_desc)
                details_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                details_item.setFlags(details_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.srv_t.setItem(r, 2, details_item)

                self.srv_t.setItem(r, 3, make_item(f"₱{price:,.2f}"))

                status_container = QWidget()
                status_container.setStyleSheet("background: transparent;")
                status_layout = QHBoxLayout(status_container)
                status_layout.setContentsMargins(0, 0, 0, 0)
                status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                lbl_status = QLabel(status)
                lbl_status.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                lbl_status.setStyleSheet("""
                    QLabel {
                        color: #f97316;
                        background: transparent;
                        border: none;
                    }
                """)
                status_layout.addWidget(lbl_status)
                self.srv_t.setCellWidget(r, 4, status_container)

                b = QPushButton("Complete")
                b.setFixedSize(110, 34)
                b.setCursor(Qt.CursorShape.PointingHandCursor)
                b.setStyleSheet("""
                    QPushButton {
                        background-color: #d1fae5;
                        color: #047857;
                        border: 1px solid #a7f3d0;
                        border-radius: 6px;
                        font-weight: bold;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background-color: #a7f3d0;
                        color: #065f46;
                    }
                """)
                b.clicked.connect(lambda _, x=sid: self.on_mark_complete_clicked(x))

                w = QWidget()
                l = QHBoxLayout(w)
                l.setAlignment(Qt.AlignmentFlag.AlignCenter)
                l.setContentsMargins(0, 0, 0, 0)
                l.addWidget(b)
                w.setStyleSheet("background:transparent;")
                self.srv_t.setCellWidget(r, 5, w)

                bd = QPushButton("Delete")
                bd.setFixedSize(110, 34)
                bd.setCursor(Qt.CursorShape.PointingHandCursor)
                bd.setStyleSheet("""
                    QPushButton {
                        background: #fee2e2;
                        color: #b91c1c;
                        border: 1px solid #fecaca;
                        border-radius: 6px;
                        font-weight: bold;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background: #fca5a5;
                        color: #7f1d1d;
                    }
                """)
                bd.clicked.connect(lambda _, x=sid: self.on_delete_service_clicked(x))

                w2 = QWidget()
                l2 = QHBoxLayout(w2)
                l2.setAlignment(Qt.AlignmentFlag.AlignCenter)
                l2.setContentsMargins(0, 0, 0, 0)
                l2.addWidget(bd)
                w2.setStyleSheet("background:transparent;")
                self.srv_t.setCellWidget(r, 6, w2)

        except Exception as e:
            print("Services Error:", e)

    def refresh_sales(self):
        try:
            sales = self.controller.get_all_sales()
            self.sal_t.setRowCount(0)

            for row_data in sales:
                date, cust, item, qty, total, payment, bank = row_data
                r = self.sal_t.rowCount()
                self.sal_t.insertRow(r)

                def make_item(text):
                    it = QTableWidgetItem(str(text) if text else "N/A")
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    return it

                self.sal_t.setItem(r, 0, make_item(str(date)))
                self.sal_t.setItem(r, 1, make_item(cust))
                self.sal_t.setItem(r, 2, make_item(item))
                self.sal_t.setItem(r, 3, make_item(str(qty)))
                self.sal_t.setItem(r, 4, make_item(f"₱{total:,.2f}"))
                self.sal_t.setItem(r, 5, make_item(payment))
                self.sal_t.setItem(r, 6, make_item(bank if bank else "N/A"))

        except Exception as e:
            print("Sales Error:", e)

    def refresh_history(self):
        try:
            history = self.controller.get_completed_services(self.controller.current_history_page)
            total_pages = self.controller.get_total_history_pages()
            self.lbl_page.setText(f"Page {self.controller.current_history_page + 1} of {total_pages}")
            self.btn_prev.setEnabled(self.controller.current_history_page > 0)
            self.btn_next.setEnabled(self.controller.current_history_page < total_pages - 1)

            self.hist_t.setRowCount(0)

            for row in history:
                cid, cname, svc_type, desc, start, end, price = row
                r = self.hist_t.rowCount()
                self.hist_t.insertRow(r)
                self.hist_t.setRowHeight(r, 50)

                def make_item(text):
                    it = QTableWidgetItem(str(text))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    return it

                self.hist_t.setItem(r, 0, make_item(str(end)))
                self.hist_t.setItem(r, 1, make_item(cname))
                self.hist_t.setItem(r, 2, make_item(svc_type))

                container = QWidget()
                container.setStyleSheet("background: transparent;")
                layout = QHBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                lbl_status = QLabel("Completed")
                lbl_status.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                lbl_status.setStyleSheet("""
                    QLabel {
                        color: #059669;
                        background: transparent;
                        border: none;
                    }
                """)
                layout.addWidget(lbl_status)
                self.hist_t.setCellWidget(r, 3, container)

                self.hist_t.setItem(r, 4, make_item(f"₱{price:,.2f}"))
                self.hist_t.setItem(r, 5, make_item(str(start)))

        except Exception as e:

            print("History Error:", e)
