## COMPY

Ця система призначена для аналізу Центру забезпечення безпеки (SOC), який потребує відстеження відповідності проектів на основі конкретних фреймворків.

Підтримується кілька фреймворків на один проект, і є можливість імпорту власних фреймворків, що відповідають потребам вашої організації.

Наразі підтримуються такі фреймворки:

- SAMA_CRF
- Regulation_S_AM
- PCI_DSS_v3.2.1
- NYCRR
- NIST_800_171
- NIST_800_53
- IT_Act_India
- ISO_27002
- ISO_27001
- ISO_22301
- hongkong_SFC_internet_trading
- HITRUST_CSF
- HIPPA_HITRUST
- GDPR
- FFIEC
- CIS_Controls_V7.1
- Canada
- Australia_APRA_cpg_234
- pci_3.1
- cisv8
- ssf
- asvs_v4.0.1
- nist_csf_v1.1
- nist_800_53_v4
- hipaa
- iso27001
- soc2
  
> Більше за все, більшість контрольних елементів потребують оновлення правильною інформацією, і це завдання, яке я виконую на даний момент - фактично одна з основних функцій полягає в тому, щоб мати можливість автоматично оновлювати контрольні елементи, оскільки це основна функція відповідності. Що варта відповідність, якщо контрольні елементи, які діють, застарілі, правда ж?

Процес налаштування цієї системи простий:

`$ docker-compose up`

Увійдіть за допомогою /admin/ за допомогою облікових записів користувачів за замовчуванням.

```
Ім'я користувача: admin
Пароль: Admin!#%135
```

Перейдіть до проектів відповідності в лівому меню навігації, натисніть "Додати фреймворк" і створіть фреймворк.

Ця програма підтримує проекти, які повинні відповідати декільком фреймворкам, що зазвичай не є обов'язковим, лише для більш професійних налаштувань.

Для кожного проекту ви можете створювати докази (наприклад, звіти про проблеми), завантажувати докази у форматі .pdf, .txt та інших і пов'язувати їх з контрольними елементами кожного фреймворку.

Ви можете включити людей до роботи над доказами, і їх можна відмічати як вирішені, коли завершено. Контрольні елементи фреймворку для кожного доказу можна додавати і видаляти, що дозволяє вам додавати контрольні елементи фреймворку інших фреймворків до проектів одного або декількох різних фреймворків на кожен проект.

Таким чином, якщо проект повинен відповідати HIPPA та SOC, ви можете працювати над тим, щоб впевнитися, що всі докази з контрольними елементами цих двох фреймворків включені.

Ще багато роботи перед нами, але це гарна вихідна точка для управління відповідностю.

Все базується на адміністраторі Django.

