# Create a bitcoin multisignature paper wallet with variable m-of-n settings..
# fpdf only allows import of images as files, therefore slightly cumbersome file writing...
from bitcoin import *
from qrcode import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from fpdf import FPDF

jpeg = 'light2.jpg'
#return a qrcode img for a bitcoin address
def qrc(address):
    qr = QRCode(box_size=3, border=3,error_correction=ERROR_CORRECT_Q)
    qr.add_data(address)
    qrim = qr.make_image()
    qrim_w, qrim_h = qrim.size
    return qrim, qrim_h, qrim_w

class NewPdf():         #create a fragment of multisig key on a single page..
    def __init__(self,n):
        self=FPDF('P','mm','A4')
        self.add_page()
        self.set_font('Times', '', 20)
        self.image(jpeg,0,0,210,297)
        self.multi_cell(0, 10,str(mkeys) + '-of-' +str(nkeys) +' : multisignature bitcoin paper wallet\ncontains private key number '+str(x+1)+' of '+str(nkeys),1,1,'C')

        self.set_font_size(16)
        self.cell(0, 130, 'multisig address: ' + addr_multi,0,1,'C')
        im, im_h, im_w = qrc(addr_multi)
        img = Image.new( 'RGB', (im_w,im_h), "white")
        img.paste(im,(0,0))
        ran=random_key()
        img.save('qrcode' + ran + '.jpg')
        self.image('qrcode' + ran + '.jpg',80,36,50,50)
        os.remove('qrcode'+ ran +'.jpg')

        self.cell(0,20,wif[n],0,1,'C')
        im, im_h, im_w = qrc(wif[n])
        img = Image.new( 'RGB', (im_w,im_h), "white")
        img.paste(im,(0,0))
        ran=random_key()
        img.save('qrcode'+ ran +'.jpg')
        self.image('qrcode'+ ran +'.jpg',80,110,50,50)
        os.remove('qrcode'+ ran +'.jpg')


        self.set_font('Times',"",10)
        self.multi_cell(0, 10, 'multisig script: ' + script,1,1)



        self.output('mspw'+str(n+1)+'.pdf','F')
        self.close()


print '>>> Multi-signature paper wallet creator <<<'
print 'How many keyholders for the multisignature address(n)?'
nkeys = int(raw_input())
if nkeys > 12:
    print 'n cannot be greater than 12'
    exit()
#need error for no number input..or if only one key
print 'How many keys required to spend funds at the address(m)?'
mkeys = int(raw_input())
if mkeys > nkeys:
    print 'm cannot be greater than n'
    exit()

print 'How many of', nkeys, 'private keys do you wish to generate randomly now? (must be',nkeys, 'or below, enter for all freshly generated keys)'
rankeys = raw_input()
if not rankeys:
    rankeys = nkeys
rankeys = int(rankeys)

priv = []
wif = []
pub = []

if rankeys > 0:
    print '>>>Generating', rankeys, 'random keys..'
    for x in range(0,rankeys):
        priv.append(random_key())

if nkeys-rankeys > 0:
    print 'Please supply', nkeys-rankeys, 'private keys..(paste a key then hit enter)'
    for x in range(0,(nkeys-rankeys)):
        print 'Paste private key number', x+1
        priv.append(raw_input())    #add error checking for bitcoin address

for x in range(0,nkeys):
    wif.append(encode_privkey(priv[x],'wif'))
    pub.append(privtopub(priv[x]))

print '>>>Creating a multi sig transaction (m-of-n):', mkeys, 'of', nkeys
script = mk_multisig_script(pub, mkeys, nkeys)
addr_multi = scriptaddr(script)

print '>>>multisig bitcoin receiving address:', addr_multi
print '>>>private keys:  '
for x in range(len(priv)):
    print x+1, priv[x]
    print pub[x]
print '>>>multisignature script:', script
print '>>>Creating paper wallet image file..'

##############################

pdf=FPDF('P','mm', 'A4')
pdf.add_page()
pdf.set_font('Times', '', 20)
pdf.image(jpeg,0,0,210,297)      #dimensions of a4 in mm
pdf.cell (0, 10,str(mkeys)+'-of-'+str(nkeys)+': multisignature bitcoin paper wallet',1,1,'C')
pdf.set_font_size(13)
pdf.cell(0, 32, 'multisig address: ' + addr_multi,1,1)

im, im_h, im_w = qrc(addr_multi)
img = Image.new( 'RGB', (im_w,im_h), "white")
img.paste(im,(0,0))
img.save('qrcode.jpg')
h_qr = 21
pdf.image('qrcode.jpg',169,h_qr,30,30)
h_qr +=1

for x in range(len(priv)):
    h_qr+=31
    pdf.cell(0,31,str(x+1)+': '+wif[x],1,1,'L')
    im, im_h, im_w = qrc(wif[x])
    img = Image.new( 'RGB', (im_w,im_h), "white")
    img.paste(im,(0,0))
    img.save('qrcode'+str(x)+'.jpg')
    pdf.image('qrcode'+str(x)+'.jpg',169,h_qr,30,29)
    os.remove('qrcode'+str(x)+'.jpg')
    if x == 6:                                           #wrapped onto the 2nd page..
        pdf.add_page()
        pdf.image('light2.jpg',0,0,210,297)
        h_qr = -20

pdf.set_font('Times',"",10)
pdf.multi_cell(0, 10, 'multisig script: ' + script,1,1)
os.remove('qrcode.jpg')
pdf.output('mspw.pdf','F')

print 'Do you want wallet file in distributable fragments?(enter for yes, all other input = no)'
dist=raw_input()
if not dist:
    print '>>>Producing separate wallets for each private key'
    for x in range(len(priv)):
        NewPdf(x)     #instantiate class for each new pdf and fill..


