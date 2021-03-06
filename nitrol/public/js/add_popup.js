var Ext;
Ext.ns('Ext.nitrol');

Ext.apply(Ext.form.VTypes, {
		num: function (v, f) {
			return /^[0-9]+$/.test(v);
		},
		numText: 'Wymagana wartość liczbowa',

		rank: function (v, f) {
			return /^[0-9]{1,2}(k|d)$/.test(v);
		},
		rankText: 'Podaj prawidłowy ranking np: 6k, 2d',

		emailText: 'Niepoprawny adres e-mail'
	});

Ext.nitrol.AddPopup = Ext.extend(Ext.Window, {
		initComponent: function () {
			this.form = new Ext.form.FormPanel({
					items: [
						new Ext.form.Hidden({itemId: 'pin', name: 'pin'}),
						new Ext.form.TextField({itemId: 'email', name: 'email', fieldLabel: 'E-mail', 
								anchor: '100%', vtype: 'email', allowBlank: false, 
								blankText: 'Adres email wymagany do potwierdzenia. Nie będzie publikowany'
							}),
						this.combo = new Ext.form.ComboBox({itemId: 'last_name',
								name: 'last_name', 
								fieldLabel: 'Nazwisko', 
								anchor: '100%', 
								allowBlank: false, 
								blankText: 'Wymagane',
								triggerAction: 'all',
								displayField: 'last_name', 
								minChars: 2,
								tpl: new Ext.XTemplate('<tpl for="."><div class="search-item">',
									'<div class="name-div">{last_name} {first_name}</div>',
									'<div class="data-div">Klub: <em>{club}</em> Siła: <em>{rank}</em></div>',
									'</div></tpl>'),
								itemSelector: 'div.search-item',
								store: new Ext.data.JsonStore({
										url: ('egd/fetchJsonData'),
										root: 'players',
										fields: [
											{name: 'pin', mapping: 'Pin_Player'},
											{name: 'last_name', mapping: 'Last_Name'},
											{name: 'first_name', mapping: 'Name'},
											{name: 'club', mapping: 'Club'},
											{name: 'rank', mapping: 'Grade'},
											{name: 'egf', mapping: 'Gor'},
											]
										})
							}),
						new Ext.form.TextField({
								itemId: 'first_name', name: 'first_name', fieldLabel: 'Imię', 
								anchor: '100%', allowBlank: false, blankText: 'Wymagane'
							}),
						new Ext.form.TextField({
								itemId: 'club', name: 'club', fieldLabel: 'Klub',
								anchor: '100%', allowBlank: false, blankText: 'Wymagane'
							}),
						new Ext.form.TextField({
								itemId: 'rank', name: 'rank', fieldLabel: 'Siła',
								anchor: '100%', allowBlank: false, blankText: 'Wymagane', vtype: 'rank'
							}),
						new Ext.form.TextField({
								itemId: 'egf', name: 'egf', fieldLabel: 'Punkty EGF', anchor: '100%', vtype: 'num'
							})
					],
					padding: 4
				});
			this.combo.on('select', function (c, rec, i) {
					this.form.getForm().loadRecord(rec);
				}, this);
			this.items = [this.form];
			this.buttons = [
				{
					text: 'Zapisz',
					iconCls: 'icon-accept',
					handler: this.onSubmit,
					scope: this
				}
			];
			Ext.nitrol.AddPopup.superclass.initComponent.apply(this, arguments);
			this.on('close', function() {delete Ext.nitrol.addPopup;}, this);
		},
		onSubmit: function () {
			this.form.el.mask('Zapisuję...', 'x-mask-loading');
			this.form.getForm().submit({
					url: 'players/add',
					method: 'POST',
					success: function () {
						this.close();
						Ext.nitrol.grid.store.load();
					},
					failure: function () {
						this.form.el.unmask();
					},
					scope: this
				})
		},
		title: 'Nowy gracz',
		height: 205,
		width: 400,
		layout: 'fit',
	});

