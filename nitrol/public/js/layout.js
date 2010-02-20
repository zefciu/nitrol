var Ext;
Ext.ns('Ext.nitrol');

Ext.nitrol.grid = new Ext.grid.GridPanel({
        store: new Ext.data.JsonStore({
                url: 'players/getindex',
                fields: [
                    'first_name',
                    'last_name',
             //       'email',
                    'rank',
                    'egf',
                ]
            }),
        columns: [
            {header: 'Imię', dataIndex: 'first_name'},
            {header: 'Nazwisko', dataIndex: 'last_name'},
            //{header: 'E-mail', dataIndex: 'email'},
            {header: 'Siła', dataIndex: 'rank'},
            {header: 'EGF', dataIndex: 'egf'}
        ],
        tbar: [
            {
                text: 'Nowy',
                iconCls: 'icon-add',
                handler: function () {
                    if (!Ext.isDefined(Ext.nitrol.addPopup)) {
                        Ext.nitrol.addPopup = new Ext.nitrol.AddPopup();
                        Ext.nitrol.addPopup.show();
                    } 
                }
            }
        ],
        region: 'center',
    });


Ext.onReady(function () {
        Ext.QuickTips.init();
        Ext.nitrol.vp = new Ext.Viewport({
                items: [Ext.nitrol.grid],
                layout: 'border'
            });
        Ext.nitrol.grid.store.load();
    })
