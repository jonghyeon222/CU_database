from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox, QSpinBox, QComboBox
from db_module import DB, DB_CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("회원 관리")
        self.db = DB(**DB_CONFIG)

        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)

        self.input_feature = QComboBox(self)
        self.input_feature.addItems(["추가", "제거", "수정"])
        self.input_feature.currentIndexChanged.connect(self.update_ui)

        form_box = QHBoxLayout()
        self.input_type = QLineEdit()
        self.input_product = QLineEdit()
        self.input_price = QLineEdit()
        self.input_tag = QLineEdit()
        self.input_stock = QSpinBox()
        self.input_stock.setRange(0, 999)
        self.btn_add = QPushButton("적용")
        self.btn_add.clicked.connect(self.apply)

        form_box.addWidget(self.input_feature)
        form_box.addWidget(QLabel("종류"))
        form_box.addWidget(self.input_type)
        form_box.addWidget(QLabel("상품명"))
        form_box.addWidget(self.input_product)
        form_box.addWidget(QLabel("가격"))
        form_box.addWidget(self.input_price)
        form_box.addWidget(QLabel("태그"))
        form_box.addWidget(self.input_tag)
        form_box.addWidget(QLabel("수량"))
        form_box.addWidget(self.input_stock)
        form_box.addWidget(self.btn_add)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Type", "Product", "Price", "Tag", "Stock"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        vbox.addLayout(form_box)
        vbox.addWidget(self.table)

        self.load_products()

    def load_products(self):
        rows = self.db.fetch_products()
        self.table.setRowCount(len(rows))
        for row, (id, type, product, price, tag, stock) in enumerate(rows):
            self.table.setItem(row, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row, 1, QTableWidgetItem(type))
            self.table.setItem(row, 2, QTableWidgetItem(product))
            self.table.setItem(row, 3, QTableWidgetItem(str(price)))
            self.table.setItem(row, 4, QTableWidgetItem(tag))
            self.table.setItem(row, 5, QTableWidgetItem(str(stock)))
        self.table.resizeColumnsToContents()

    def add_product(self):
        type = self.input_type.text().strip()
        product = self.input_product.text().strip()
        price = self.input_price.text().strip()
        tag = self.input_tag.text().strip()
        stock = self.input_stock.text().strip()
        if not type or not product or not price or not tag or not stock:
            QMessageBox.warning(self, "오류", "모든 정보를 입력하세요.")
            return
        ok1 = self.db.verify_products(product)
        if not ok1:
            ok2 = self.db.insert_product(type, product, price, tag, stock)
            if ok2:
                QMessageBox.information(self, "완료", "추가되었습니다.")
                self.input_type.clear()
                self.input_product.clear()
                self.input_price.clear()
                self.input_tag.clear()
                self.input_stock.clear()
                self.load_products()
            else:
                QMessageBox.critical(self, "실패", "추가 중 오류가 발생했습니다.")
        else:
            QMessageBox.critical(self, "실패", "상품이 이미 존재합니다.")

    def del_product(self):
        product = self.input_product.text().strip()
        if not product:
            QMessageBox.warning(self, "오류", "제거할 상품명을 입력하세요.")
            return
        ok1 = self.db.verify_products(product)
        if ok1:
            ok2 = self.db.delete_product(product)
            if ok2:
                QMessageBox.information(self, "완료", "제거되었습니다.")
                self.input_product.clear()
                self.load_products()
            else:
                QMessageBox.critical(self, "실패", "제거 중 오류가 발생했습니다.")
        else:
            QMessageBox.critical(self, "실패", "상품이 존재하지 않습니다.")

    def apply(self):
        func = self.input_feature.currentText()
        if func == "추가":
            self.add_product()
        elif func == "제거":
            self.del_product()
        elif func == "수정":
            pass

    def update_ui(self):
        func = self.input_feature.currentText()
        if func == "추가":
            self.input_type.setEnabled(True)
            self.input_product.setEnabled(True)
            self.input_price.setEnabled(True)
            self.input_tag.setEnabled(True)
            self.input_stock.setEnabled(True)
        elif func == "제거":
            self.input_type.setEnabled(False)
            self.input_product.setEnabled(True)
            self.input_price.setEnabled(False)
            self.input_tag.setEnabled(False)
            self.input_stock.setEnabled(False)
        elif func == "수정":
            self.input_type.setEnabled(False)
            self.input_product.setEnabled(True)
            self.input_price.setEnabled(True)
            self.input_tag.setEnabled(False)
            self.input_stock.setEnabled(True)

