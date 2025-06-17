from PySide6.QtWidgets import QMainWindow, QTabWidget
from product_master import ProductMasterForm
from goods_receiving import GoodsReceivingForm
from sales import SalesForm

class MainWindow(QMainWindow):
    """Main application window with tabbed interface"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self._initialize_ui()
        
    def _initialize_ui(self):
        """Set up window properties and tabs"""
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 1024, 768)  # x, y, width, height
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Initialize forms with database connection
        self.product_master_tab = ProductMasterForm(self.db_manager)
        self.goods_receiving_tab = GoodsReceivingForm(self.db_manager)
        self.sales_tab = SalesForm(self.db_manager)
        
        # Add tabs
        tab_widget.addTab(self.product_master_tab, "&Product Master")
        tab_widget.addTab(self.goods_receiving_tab, "&Goods Receiving")
        tab_widget.addTab(self.sales_tab, "&Sales")
        
        # Set as central widget
        self.setCentralWidget(tab_widget)

# Test block (remove in production)
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    from database import DatabaseManager
    
    app = QApplication(sys.argv)
    db = DatabaseManager()
    window = MainWindow(db)
    window.show()
    sys.exit(app.exec())
