var Ext;
Ext.ns('Ext.nitrol');

Ext.form.VTypes.emailText = 'Niepoprawny adres e-mail';

Ext.nitrol.AddPopup = Ext.extend(Ext.Window, {
        initComponent: function () {
            this.nameTab = new Ext.form.FormPanel({
                    items: [
                        new Ext.form.TextField({
                                id: 'first_name', name: 'first_name', fieldLabel: 'Imię', 
                                anchor: '100%', allowBlank: false, blankText: 'Wymagane'
                            }),
                        new Ext.form.TextField({id: 'last_name', name: 'last_name', fieldLabel: 'Nazwisko', 
                                anchor: '100%', allowBlank: false, blankText: 'Wymagane'
                            }),
                        new Ext.form.TextField({id: 'email', name: 'email', fieldLabel: 'E-mail', 
                                anchor: '100%', vtype: 'email', allowBlank: false, 
                                blankText: 'Adres email wymagany do potwierdzenia. Nie będzie publikowany'
                            })
                    ],
                    
                    buttons: [
                        {
                            text: 'Dalej',
                            iconCls: 'icon-arrow_right',
                        }
                    ],
                    title: 'Dane',
                    padding: 4
                });
            this.rankTab = new Ext.form.FormPanel({
                    disabled: true,
                    title: 'Siła'
                });
            this.items = [this.tp = new Ext.TabPanel({items: [this.nameTab, this.rankTab]})],
            Ext.nitrol.AddPopup.superclass.initComponent.apply(this, arguments);
            this.tp.setActiveTab(this.nameTab);
            this.on('close', function() {delete Ext.nitrol.addPopup;}, this);
        },
        title: 'Nowy gracz',
        height: 300,
        width: 400,
        layout: 'fit',
    });

