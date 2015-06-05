import os, sys, time
from PyQt4 import QtGui, QtCore
import collections
import encdec

class PopupDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.initUI()

    def initUI(self):

        self.label_error = QtGui.QLabel()
        self.label_error.setFont(QtGui.QFont('Decorative', 10))

        okButton = QtGui.QPushButton("OK")
        okButton.clicked.connect(self.close)

        center(self)

        hori = QtGui.QHBoxLayout()
        hori.addStretch(1)
        hori.addWidget(self.label_error)
        hori.addStretch(1)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hori)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 270, 150)
        self.setWindowTitle('Error!')

    def setval(self, errorval):
        self.label_error.setText(errorval)


class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        #Window propoerties
        self.setGeometry(0,0,500,550)
        self.setWindowTitle("Elliptic Curve Cryptography - ElGamal")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.resize(500,550)
        self.setMinimumSize(500,550)
        center(self)
         
        #Tabs in the GUI
        self.tab_widget = QtGui.QTabWidget()
        #For encryption
        tab1 = QtGui.QWidget()
        #For decryption
        tab2 = QtGui.QWidget()
        #For defining curve
        tab0 = QtGui.QWidget()

        #Layouts for tabs
        p0_vertical = QtGui.QVBoxLayout(tab0)
        p1_vertical = QtGui.QVBoxLayout(tab1)
        p2_vertical = QtGui.QVBoxLayout(tab2)
        
        self.bar = QtGui.QStatusBar(self)
        self.bar.showMessage("Ready. Define curve to begin.")

        #add tabs, name them
        self.tab_widget.addTab(tab0, "Curve")
        self.tab_widget.addTab(tab1, "Encrypt")
        self.tab_widget.addTab(tab2, "Decrypt")
        self.tab_widget.setTabEnabled(1,False)
        self.tab_widget.setTabEnabled(2,False)

        #labels for Tab 1
        eqn_label = QtGui.QLabel("Equation : y\xb2 mod q = (x\xb3 + ax + b) mod q ")
        eqn_label.setMinimumHeight(50)
        eqn_label.setAlignment(QtCore.Qt.AlignCenter)
        eqn_label.setFont(QtGui.QFont('Decorative', 13))

        label_a = QtGui.QLabel("Enter value of a:")
        label_b = QtGui.QLabel("Enter value of b:")
        label_c = QtGui.QLabel("Enter value of q (Prime number):")
        label_priv = QtGui.QLabel("Enter the private key (Not necesary):")
        label_message = QtGui.QLabel("Enter the message you want to encrypt:")
        label_pub = QtGui.QLabel("Enter public key of recipient:")
        label_encrypted = QtGui.QLabel("The encrypted data is:")
        label_decrypted = QtGui.QLabel("The decrypted data is:")
        publickey = QtGui.QLabel("The public key is:")

        self.write_encrypted = QtGui.QCheckBox("Write encrypted data to file")
        self.write_decrypted = QtGui.QCheckBox("Write decrypted data to file")

        browseButton = QtGui.QPushButton("Browse")
        browseButton.clicked.connect(lambda: self.showDialog(1))
        self.destTextField = QtGui.QTextEdit()
        self.destTextField.setMaximumHeight(label_a.sizeHint().height()*2)
        self.destTextField.setReadOnly(True)

        #Textboxes for Tab 1  
        self.val_a = QtGui.QTextEdit()
        self.val_a.setTabChangesFocus(True)

        self.val_b = QtGui.QTextEdit()
        self.val_b.setTabChangesFocus(True)

        self.val_c = QtGui.QTextEdit()
        self.val_c.setTabChangesFocus(True)

        self.val_priv = QtGui.QTextEdit()
        self.val_priv.setTabChangesFocus(True)

        self.msg_val = QtGui.QTextEdit()
        self.msg_val.setTabChangesFocus(True)

        self.val_pub = QtGui.QTextEdit()
        self.val_pub.setTabChangesFocus(True)

        self.public = QtGui.QTextEdit()
        self.public.setReadOnly(True)

        self.encrypted_string = QtGui.QTextEdit()
        self.encrypted_string.setTabChangesFocus(True)

        self.decrypted_string = QtGui.QTextEdit()
        self.decrypted_string.setTabChangesFocus(True)

        #button for curve generation, accompanying Label
        button = QtGui.QPushButton("Generate Curve")
        button.clicked.connect(self.generateCurve)

        button_enc = QtGui.QPushButton("Encrypt Data")
        button_enc.clicked.connect(self.encryptData)

        hori_box = QtGui.QHBoxLayout()
        hori_box.addWidget(self.destTextField)
        hori_box.addWidget(browseButton)

        browseButton2 = QtGui.QPushButton("Browse")
        browseButton2.clicked.connect(lambda: self.showDialog(2))

        self.destTextField2 = QtGui.QTextEdit()
        self.destTextField2.setMaximumHeight(label_a.sizeHint().height()*2)
        self.destTextField2.setReadOnly(True)

        hori_box2 = QtGui.QHBoxLayout()
        hori_box2.addWidget(self.destTextField2)
        hori_box2.addWidget(browseButton2)

        #add elements to Tab 1
        p0_vertical.addWidget(eqn_label)
        p0_vertical.addWidget(label_a)
        p0_vertical.addWidget(self.val_a)
        p0_vertical.addWidget(label_b)
        p0_vertical.addWidget(self.val_b)
        p0_vertical.addWidget(label_c)
        p0_vertical.addWidget(self.val_c)
        p0_vertical.addWidget(label_priv)
        p0_vertical.addWidget(self.val_priv)
        p0_vertical.addWidget(button)
        p0_vertical.addWidget(publickey)
        p0_vertical.addWidget(self.public)
        p0_vertical.addStretch(1)

        p1_vertical.addWidget(label_pub)
        p1_vertical.addWidget(self.val_pub)
        p1_vertical.addWidget(label_message)
        p1_vertical.addLayout(hori_box)
        p1_vertical.addWidget(self.msg_val)
        p1_vertical.addWidget(self.write_encrypted)
        p1_vertical.addWidget(button_enc)
        p1_vertical.addWidget(label_encrypted)
        p1_vertical.addWidget(self.encrypted_string)

        #Labels for Tab 2
        label_key = QtGui.QLabel("Enter your private key:")
        label_enc_message = QtGui.QLabel("Enter the Encrypted message:")

        #Buttons for Tab 2
        button_dec = QtGui.QPushButton("Decrypt Data")
        button_dec.clicked.connect(self.decryptData)

        #Textboxes for Tab 2
        self.priv_key = QtGui.QTextEdit()
        self.priv_key.setTabChangesFocus(True)

        self.encrypted_data = QtGui.QTextEdit()
        self.encrypted_data.setTabChangesFocus(True)

        #Set height for textboxes
        self.val_a.setMaximumHeight(label_a.sizeHint().height()*2)
        self.val_b.setMaximumHeight(label_b.sizeHint().height()*2)
        self.val_c.setMaximumHeight(label_c.sizeHint().height()*2)
        self.val_priv.setMaximumHeight(label_c.sizeHint().height()*2)
        self.msg_val.setMaximumHeight(label_c.sizeHint().height()*6)
        self.public.setMaximumHeight(label_b.sizeHint().height()*2)
        self.val_pub.setMaximumHeight(label_priv.sizeHint().height()*2)
        self.priv_key.setMaximumHeight(label_priv.sizeHint().height()*2)
        self.encrypted_data.setMaximumHeight(label_priv.sizeHint().height()*6)
        self.encrypted_string.setMaximumHeight(label_priv.sizeHint().height()*20)
        self.decrypted_string.setMaximumHeight(label_priv.sizeHint().height()*20)

        #Adding widgets to Tab 2
        p2_vertical.addWidget(label_key)
        p2_vertical.addWidget(self.priv_key)
        p2_vertical.addWidget(label_enc_message)
        p2_vertical.addLayout(hori_box2)
        p2_vertical.addWidget(self.encrypted_data)
        p2_vertical.addWidget(self.write_decrypted)
        p2_vertical.addWidget(button_dec)
        p2_vertical.addWidget(label_decrypted)
        p2_vertical.addWidget(self.decrypted_string)

        self.tab_widget.currentChanged.connect(self.currentTabChanged)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tab_widget)
        vbox.addWidget(self.bar)
        self.setLayout(vbox)

    def currentTabChanged(self):
        if self.tab_widget.currentIndex() == 1:
            self.bar.showMessage("Encrypt Tab. Ready.")
            if self.key is not None:
                self.val_pub.setText(self.key)
            else:
                self.val_pub.setText("")
            self.val_pub.clearFocus()
        elif self.tab_widget.currentIndex() == 2:
            self.bar.showMessage("Decrypt Tab. Ready.")
            if self.priv != -1:
                self.priv_key.setText(str(self.priv))
            else:
                self.priv_key.setText("")
            self.priv_key.clearFocus()
        elif self.tab_widget.currentIndex() == 0:
            self.bar.showMessage("Curve tab. You can define a new curve if you want.")

    def showDialog(self, value):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'C:')
        if value == 1 and fname:
            self.destTextField.setPlainText(fname)
            self.write_encrypted.setCheckState(2)
        elif value == 2 and fname:
            self.destTextField2.setPlainText(fname)
            self.write_decrypted.setCheckState(2)
        f = open(fname, 'r')
        with f:        
            data = f.read()
            if value == 1:
                self.msg_val.setText(data)
            elif value == 2:
                self.encrypted_data.setText(data)

    def generateCurve(self):
        try:
            self.a = int(self.val_a.toPlainText())
            self.b = int(self.val_b.toPlainText())
            self.q = int(self.val_c.toPlainText())
        except:
            self.popup("Please input numbers in the necessary fields!")
            return
        self.priv = int(self.val_priv.toPlainText() or -1)
        self.ed = encdec.Values()
        try:
            self.key = self.ed.public_key(self.a, self.b, self.q, self.priv)
        except:
            self.popup("Not a valid curve! Please define a valid curve.")
        if self.key is not None:
            self.public.setText(self.key)
        else:
            self.public.setText("")
        self.tab_widget.setTabEnabled(1,True)
        self.tab_widget.setTabEnabled(2,True)
        self.bar.showMessage("Curve defined! Move to Encrypt or Decrypt tabs for more.")

    def encryptData(self):
        try:
            pub_raw = str(self.val_pub.toPlainText())
            message = self.msg_val.toPlainText()
        except:
            self.popup("Something's wrong, I can feel it.")
            return
        self.bar.showMessage("Encrypting...")
        
        encrypted_text = self.ed.encryption(pub_raw, message)
        self.encrypted_string.setText(encrypted_text)
        
        message_to_show = "Encrypted!"

        if self.write_encrypted.isChecked():
            path = 'encrypted.txt'
            path_acq = str(self.destTextField.toPlainText())
            if path_acq:
                index_path = path_acq.rfind(".")
                if index_path != -1:
                    path = path_acq[:index_path] + ".enc." + path_acq[index_path+1:]

            with open(path, 'w+') as f:
                f.write(encrypted_text)
                message_to_show = "Encrypted. File saved at " + path 
            
        self.bar.showMessage(message_to_show)
            

    def decryptData(self):
        try:
            private_key = int(self.priv_key.toPlainText())
            cipher_raw = str(self.encrypted_data.toPlainText())
        except:
            self.popup("Error encountered. Please call Vodafone.")
            return
        self.bar.showMessage("Decrypting...")

        finalval = self.ed.decryption(private_key, cipher_raw)
        self.decrypted_string.setText(finalval)

        message_to_show = "Decrypted!"
        
        if self.write_decrypted.isChecked():
            path_acq = str(self.destTextField2.toPlainText())
            path = 'decrypted.txt'
            if path_acq:
                index_path = path_acq.rfind(".enc")
                if index_path != -1:
                    path = path_acq[:index_path] + ".dec" + path_acq[index_path+4:]
                else:
                    index_path = path_acq.rfind(".")
                    if index_path != -1:
                        path = path_acq[:index_path] + ".dec." + path_acq[index_path+1:]

            with open(path, 'w+') as f:
                f.write(finalval)
                message_to_show = "Decrypted. File saved at " + path
            
        self.bar.showMessage(message_to_show)

    def popup(self, errorval):
        self.dialog = PopupDialog()
        self.dialog.setval(errorval)
        self.dialog.show()

#Start window in the center of the screen
def center(widget): 
    screen = QtGui.QDesktopWidget().screenGeometry()
    size = widget.geometry()
    widget.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

app = QtGui.QApplication(sys.argv)
frame = MainWindow()
frame.show()
sys.exit(app.exec_())
