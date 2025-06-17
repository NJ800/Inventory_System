from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox

class SalesForm(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        self.barcode = QLineEdit()
        self.customer_name = QLineEdit()
        self.customer_address = QLineEdit()
        self.quantity = QLineEdit()
        self.unit = QComboBox()
        self.unit.addItems(["Piece", "Kg", "Liter", "Meter"])
        self.rate = QLineEdit()
        self.tax = QLineEdit()
        self.submit_btn = QPushButton("Record Sale")
        self.submit_btn.clicked.connect(self.submit)
        layout.addRow("Barcode:", self.barcode)
        layout.addRow("Customer:", self.customer_name)
        layout.addRow("Address:", self.customer_address)
        layout.addRow("Quantity:", self.quantity)
        layout.addRow("Unit:", self.unit)
        layout.addRow("Rate:", self.rate)
        layout.addRow("Tax (%):", self.tax)
        layout.addRow(self.submit_btn)
        self.setLayout(layout)
    
    def submit(self):
        try:
            qty = float(self.quantity.text())
            rate = float(self.rate.text())
            tax_pct = float(self.tax.text())
            subtotal = qty * rate
            tax_amt = subtotal * (tax_pct / 100)
            total = subtotal + tax_amt
            cursor = self.db.get_connection().cursor()
            cursor.execute('''
                INSERT INTO SalesForm (
                    product_barcode, customer_name, customer_address,
                    quantity, unit, rate, total, tax
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.barcode.text(),
                self.customer_name.text(),
                self.customer_address.text(),
                qty,
                self.unit.currentText(),
                rate,
                total,
                tax_amt
            ))
            self.db.get_connection().commit()
            QMessageBox.information(self, "Success", "Sale recorded!")
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def clear_fields(self):
        for field in [self.barcode, self.customer_name, self.customer_address, self.quantity, self.rate, self.tax]:
            field.clear()
