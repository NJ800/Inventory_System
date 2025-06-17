from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QComboBox, QPushButton, QFileDialog, QMessageBox

class ProductMasterForm(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        self.barcode = QLineEdit()
        self.sku = QLineEdit()
        self.category = QComboBox()
        self.category.addItems(["Electronics", "Clothing", "Groceries", "Office"])
        self.subcategory = QLineEdit()
        self.images = QLineEdit()
        self.browse_btn = QPushButton("Browse Images")
        self.browse_btn.clicked.connect(self.browse_images)
        self.name = QLineEdit()
        self.desc = QLineEdit()
        self.tax = QLineEdit()
        self.price = QLineEdit()
        self.unit = QComboBox()
        self.unit.addItems(["Piece", "Kg", "Liter", "Meter"])
        self.submit_btn = QPushButton("Add Product")
        self.submit_btn.clicked.connect(self.submit)
        layout.addRow("Barcode:", self.barcode)
        layout.addRow("SKU:", self.sku)
        layout.addRow("Category:", self.category)
        layout.addRow("Subcategory:", self.subcategory)
        layout.addRow("Images:", self.images)
        layout.addRow("", self.browse_btn)
        layout.addRow("Name:", self.name)
        layout.addRow("Description:", self.desc)
        layout.addRow("Tax (%):", self.tax)
        layout.addRow("Price:", self.price)
        layout.addRow("Unit:", self.unit)
        layout.addRow(self.submit_btn)
        self.setLayout(layout)
    
    def browse_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg)")
        if files:
            self.images.setText(";".join(files))
    
    def submit(self):
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute('''
                INSERT INTO ProductMasterList VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.barcode.text(),
                self.sku.text(),
                self.category.currentText(),
                self.subcategory.text(),
                self.images.text(),
                self.name.text(),
                self.desc.text(),
                float(self.tax.text()),
                float(self.price.text()),
                self.unit.currentText()
            ))
            self.db.get_connection().commit()
            QMessageBox.information(self, "Success", "Product added!")
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def clear_fields(self):
        for field in [self.barcode, self.sku, self.subcategory, self.images, self.name, self.desc, self.tax, self.price]:
            field.clear()
