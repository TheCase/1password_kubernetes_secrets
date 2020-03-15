## 1Password Kubernetes Secrets

### Requirement: 

- 1password CLI: [https://support.1password.com/command-line/]()

- install python requirements: 
  `pip3 install -r requirements.txt`

### Usage:

First off, make sure you have used `op signin` to create and set the token environment variable: [https://support.1password.com/command-line#sign-in-or-out]()

You'll need to create a map file (default: `field_map.yaml`) that maps 1password UUID values to the fields you want to use for secrets.  See `field_map.yaml.dist for examples.

Non-tandard fields that are not "username", "password" and "website" are field-searched from the Sections areas of the 1Password Login item.  Its possible I have not accounted for all field locations, so bug reporting would be helpful to identify and correct for such situations. Thanks!

You can use `find-uuid.py` to search for the UUID of the 1password items you wish to match:

example:

```./find-uuid.py | grep -i mysql```

Export script will output a `secrets.yaml` manifest file:

```./export-1password.py``` 


