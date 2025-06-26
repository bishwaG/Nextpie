
## Admin GUI


![](../assets/images/admin.png)


Nextpie provides an administrator interface for modifying specific database entries. It can be accessed by navigating to [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin).

This URL is not linked to or displayed within the Nextpie user interface, so administrators must manually enter it into their browser's address bar.

Any user marked as a superuser (the super_user field in the user table) can access this interface. Nextpie includes a default administrative user named admin, which cannot be deleted through the interface.

> Note: If you are running Nextpie in a production environment with a domain name or public IP address, the base URL will differ accordingly.
