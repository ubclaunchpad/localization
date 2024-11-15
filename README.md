# I18nilize
The i18n and l10n package designed for microservices
## What is it?
I18nilize is a pip package designed to make localization/internationalization easy for microservices. 
<br/>
Translations are stored by language. 
To sync data across APIs, one microservice will be assigned as the writer, while the others are readers. This ensures a constant source of truth that doesn't change. A diffing algorithm is used to detect changes in language files. 


(will finish this later)
