import requests
import xmltodict

def docsvault_login(username: str, password: str, api_url: str) -> str:
    """
    Logs into the Docsvault API and returns the Token ID for a unique session.

    Args:
        username (str): The Docsvault user name or Windows username with AD authentication used in Docsvault.
        password (str): The user's password in Docsvault or AD depending on the authentication type.
        api_url (str): The Docsvault API endpoint URL.

    Returns:
        str: The Token ID valid for a unique session.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.

    Note:
        The unique Token ID returned by this function is only valid for the current session. Once the session has
        expired, you will need to get a new Token ID before making further calls. The session timeout is set to
        20 minutes by default. You can change this by changing the value for the 'APISessionTimeout' tag in the
        web.config file located in the 'Docsvault Web' program folder.

    Raises:
        ValueError: If the API response did not contain a valid Token ID.

    """
    # Set the API action and parameters
    action = "Login"
    params = {
        "UserName": username,
        "Password": password
    }

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url + action, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "1":
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Login failed. " + error_message)

        # Extract the Token ID from the API response
        token_id = response_dict["Docsvault"]["Result"]["TokenID"]
        if token_id is None or token_id == "":
            raise ValueError("Login failed. Token ID not found in API response.")

        return token_id
    else:
        raise requests.exceptions.RequestException("Login request failed with status code: " + str(response.status_code))

def docsvault_login_post(username: str, password: str, api_url: str) -> str:
    """
    Logs into the Docsvault API using the POST method and returns the Token ID for a unique session.

    Args:
        username (str): The Docsvault user name or Windows username with AD authentication used in Docsvault.
        password (str): The user's password in Docsvault or AD depending on the authentication type.
        api_url (str): The Docsvault API endpoint URL.

    Returns:
        str: The Token ID valid for a unique session.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain a valid Token ID.

    Note:
        The unique Token ID returned by this function is only valid for the current session. Once the session has
        expired, you will need to get a new Token ID before making further calls. The session timeout is set to
        20 minutes by default. You can change this by changing the value for the 'APISessionTimeout' tag in the
        web.config file located in the 'Docsvault Web' program folder.

    Raises:
        ValueError: If the API response did not contain a valid Token ID.

    """
    # Set the API action and parameters
    action = "LoginPost"
    params = {
        "UserName": username,
        "Password": password
    }

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.post(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "1":
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Login failed. " + error_message)

        # Extract the Token ID from the API response
        token_id = response_dict["Docsvault"]["Result"]
        if token_id is None or token_id == "":
            raise ValueError("Login failed. Token ID not found in API response.")

        return token_id
    else:
        raise requests.exceptions.RequestException("Login request failed with status code: " + str(response.status_code))

def docsvault_logout(token_id: str, username: str, api_url: str) -> None:
    """
    Logs out of the Docsvault API and closes the unique session.

    Args:
        token_id (str): The unique Token ID for the current session.
        username (str): The Docsvault user name or Active Directory name used in Docsvault.
        api_url (str): The Docsvault API endpoint URL.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.

    Note:
        Once you have finished making API calls with the current session, you should call this function to log out
        of the API and close the session.

    Raises:
        ValueError: If the API response indicates an error.

    """
    # Set the API action and parameters
    action = "Logout"
    params = {
        "TokenID": token_id,
        "UserName": username
    }

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "1":
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Logout failed. " + error_message)
    else:
        raise requests.exceptions.RequestException("Logout request failed with status code: " + str(response.status_code))

def docsvault_get_login_user_id(token_id: str, api_url: str) -> str:
    """
    Gets the user ID of the user logged in Docsvault API based on Token ID.

    Args:
        token_id (str): The Token ID for a unique session.
        api_url (str): The Docsvault API endpoint URL.

    Returns:
        str: The User ID of the logged-in user.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain a valid User ID.

    """
    # Set the API action and parameters
    action = "GetLoginUserID"
    params = {
        "TokenID": token_id,
    }

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "1":
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("GetLoginUserID failed. " + error_message)

        # Extract the User ID from the API response
        user_id = response_dict["Docsvault"]["Result"]["UserID"]
        if user_id is None or user_id == "":
            raise ValueError("GetLoginUserID failed. User ID not found in API response.")

        return user_id
    else:
        raise requests.exceptions.RequestException("GetLoginUserID request failed with status code: " + str(response.status_code))

def docsvault_get_user_details_by_name(token_id: str, user_name: str, api_url: str) -> dict:
    """
    Gets the details of a user by their username in Docsvault.

    Args:
        token_id (str): The unique session ID.
        user_name (str): The Docsvault user name or Windows username with AD authentication used in Docsvault.
        api_url (str): The Docsvault API endpoint URL.

    Returns:
        dict: A dictionary containing the user details.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "UserDetails/GetUserDetailsByName"
    params = {
        "TokenID": token_id,
        "UserName": user_name
    }

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the user details from the API response
            user_detail = response_dict["Docsvault"]["Result"]["UserDetail"]

            # Return the user details as a dictionary
            return {
                "user_id": user_detail["UserID"],
                "user_name": user_detail["UserName"],
                "full_name": user_detail["UserFullName"],
                "description": user_detail["UserDescription"],
                "email": user_detail["UserEmail"],
                "dv_authentication": user_detail["DVAuthentication"],
                "web_access": user_detail["WebAccess"],
                "license_type": user_detail["LicenseType"]
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get user details. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get user details. Status code: " + str(response.status_code))

def docsvault_get_user_details_by_id(token_id: str, user_id: str, api_url: str) -> dict:
    """
    Gets the details of a user by their user ID in Docsvault.

    Args:
        token_id (str): The unique session ID.
        user_id (str): The unique user ID in Docsvault.
        api_url (str): The Docsvault API endpoint URL.

    Returns:
        dict: A dictionary containing the user details.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "UserDetails/GetUserDetailsByID"
    params = {
        "TokenID": token_id,
        "UserID": user_id
    }

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the user details from the API response
            user_detail = response_dict["Docsvault"]["Result"]["UserDetail"]

            # Return the user details as a dictionary
            return {
                "user_id": user_detail["UserID"],
                "user_name": user_detail["UserName"],
                "full_name": user_detail["UserFullName"],
                "description": user_detail["UserDescription"],
                "email": user_detail["UserEmail"],
                "dv_authentication": user_detail["DVAuthentication"],
                "web_access": user_detail["WebAccess"],
                "license_type": user_detail["LicenseType"]
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get user details. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get user details. Status code: " + str(response.status_code))

def docsvault_get_user_details_by_email(token_id: str, email: str, api_url: str) -> dict:
    """
    Gets the details of a user by their email address in Docsvault.

    Args:
        token_id (str): The unique session ID.
        email (str): The email address of the Docsvault user.
        api_url (str): The Docsvault API endpoint URL.

    Returns:
        dict: A dictionary containing the user details.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "UserDetails/GetUserDetailsByEmailID"
    params = {
        "TokenID": token_id,
        "EmailID": email
    }

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the user details from the API response
            user_detail = response_dict["Docsvault"]["Result"]["UserDetail"]

            # Return the user details as a dictionary
            return {
                "user_id": user_detail["UserID"],
                "user_name": user_detail["UserName"],
                "full_name": user_detail["UserFullName"],
                "description": user_detail["UserDescription"],
                "email": user_detail["UserEmail"],
                "dv_authentication": user_detail["DVAuthentication"],
                "web_access": user_detail["WebAccess"],
                "license_type": user_detail["LicenseType"]
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get user details. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get user details. Status code: " + str(response.status_code))

def docsvault_get_readonly_users(token_id: str, api_url: str) -> list:
    """
    Gets a list of all users with Read Only rights in Docsvault.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.

    Returns:
        list: A list of dictionaries containing the user details.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "UserDetails/GetReadonlyUsers"
    params = {"TokenID": token_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the user details from the API response
            user_details = response_dict["Docsvault"]["Result"]["UserDetail"]

            # If there is only one user, wrap it in a list to maintain consistency
            if isinstance(user_details, dict):
                user_details = [user_details]

            # Return the user details as a list of dictionaries
            return [{
                "user_id": user_detail["UserID"],
                "user_name": user_detail["UserName"],
                "full_name": user_detail["UserFullName"],
                "description": user_detail["UserDescription"],
                "email": user_detail["UserEmail"],
                "dv_authentication": user_detail["DVAuthentication"],
                "web_access": user_detail["WebAccess"],
                "license_type": user_detail["LicenseType"]
            } for user_detail in user_details]
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get readonly users. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get readonly users. Status code: " + str(response.status_code))

def docsvault_get_webaccess_users(token_id: str, api_url: str) -> list:
    """
    Gets a list of all users with Web Access rights in Docsvault.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.

    Returns:
        list: A list of dictionaries containing the user details.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """
    # Set the API action and parameters
    action = "UserDetails/GetWebAccessUsers"
    params = {"TokenID": token_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the user details from the API response
            user_details = response_dict["Docsvault"]["Result"]["UserDetail"]

            # If there is only one user, wrap it in a list to maintain consistency
            if isinstance(user_details, dict):
                user_details = [user_details]

            # Return the user details as a list of dictionaries
            return [{
                "user_id": user_detail["UserID"],
                "user_name": user_detail["UserName"],
                "full_name": user_detail["UserFullName"],
                "description": user_detail["UserDescription"],
                "email": user_detail["UserEmail"],
                "dv_authentication": user_detail["DVAuthentication"],
                "web_access": user_detail["WebAccess"],
                "license_type": user_detail["LicenseType"]
            } for user_detail in user_details]
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get Web Access users. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get Web Access users. Status code: " + str(response.status_code))

def docsvault_get_user_groups(token_id: str, user_id: str, api_url: str) -> list:
    """
    Gets the groups of a user by passing his/her User ID.

    Args:
        token_id (str): The unique session ID.
        user_id (str): The unique user ID.
        api_url (str): The Docsvault API endpoint URL.

    Returns:
        list: A list of dictionaries containing the group details.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "UserDetails/GetUserGroup"
    params = {"TokenID": token_id, "UserID": user_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the group details from the API response
            group_details = response_dict["Docsvault"]["Result"]["Group"]

            # If there is only one group, wrap it in a list to maintain consistency
            if isinstance(group_details, dict):
                group_details = [group_details]

            # Return the group details as a list of dictionaries
            return [{
                "group_name": group_detail["GroupName"],
                "group_id": group_detail["GroupID"],
                "description": group_detail["Description"]
            } for group_detail in group_details]
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get user groups. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get user groups. Status code: " + str(response.status_code))

def docsvault_get_connected_users(token_id: str, api_url: str) -> list:
    """
    Gets a list of all currently connected users in Docsvault.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.

    Returns:
        list: A list of dictionaries containing the connected user details.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "UserDetails/GetConnectedUsers"
    params = {"TokenID": token_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the user details from the API response
            user_details = response_dict["Docsvault"]["Result"]["UserDetail"]

            # If there is only one user, wrap it in a list to maintain consistency
            if isinstance(user_details, dict):
                user_details = [user_details]

            # Return the user details as a list of dictionaries
            return [{
                "user_id": user_detail["UserID"],
                "user_name": user_detail["UserName"],
                "full_name": user_detail["UserFullName"],
                "description": user_detail["UserDescription"],
                "email": user_detail["UserEmail"],
                "dv_authentication": user_detail["DVAuthentication"],
                "web_access": user_detail["WebAccess"],
                "login_from": user_detail["LoginFrom"],
                "license_type": user_detail["LicenseType"]
            } for user_detail in user_details]
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get connected users. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get connected users. Status code: " + str(response.status_code))

def docsvault_get_user_groups(token_id: str, api_url: str, user_id: str) -> list:
    """
    Gets the groups that a user belongs to in Docsvault.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        user_id (str): The unique user ID.

    Returns:
        list: A list of dictionaries containing the user's group details.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "UserDetails/GetUserGroup"
    params = {"TokenID": token_id, "UserID": user_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the group details from the API response
            group_details = response_dict["Docsvault"]["Result"]["Group"]

            # If there is only one group, wrap it in a list to maintain consistency
            if isinstance(group_details, dict):
                group_details = [group_details]

            # Return the group details as a list of dictionaries
            return [{
                "group_name": group_detail["GroupName"],
                "group_id": group_detail["GroupID"],
                "description": group_detail["Description"]
            } for group_detail in group_details]
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get user groups. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get user groups. Status code: " + str(response.status_code))

def docsvault_get_file_details(token_id: str, api_url: str, file_id: str) -> dict:
    """
    Gets the details of a file in Docsvault.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        file_id (str): The unique file ID.

    Returns:
        dict: A dictionary containing the file details.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "FileDetails/GetFileDetailsByID"
    params = {"TokenID": token_id, "FileID": file_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the file details from the API response
            file_details = response_dict["Docsvault"]["Result"]["FileDetail"]

            # Return the file details as a dictionary
            return {
                "file_id": file_details["FileID"],
                "parent_id": file_details["ParentID"],
                "file_name": file_details["FileName"],
                "description": file_details["Description"],
                "flag_name": file_details["FlagName"],
                "file_size": file_details["FileSize"],
                "doc_type": file_details["DocType"],
                "pages": file_details["Pages"],
                "version": file_details["Version"],
                "version_note": file_details["VersionNote"],
                "version_owner": file_details["VersionOwner"],
                "version_owner_name": file_details["VersionOwnerName"],
                "modified_date": file_details["ModifiedDate"],
                "created_date": file_details["CreatedDate"],
                "accessed_date": file_details["AccessedDate"],
                "checked_out": file_details.get("CheckedOut") == "true",
                "checked_out_by": file_details.get("CheckedOutBy"),
                "checked_out_by_name": file_details.get("CheckedOutByName"),
                "owner_id": file_details["OwnerID"],
                "owner_name": file_details["OwnerName"],
                "location": file_details["Location"],
                "doc_notes": file_details["DocNotes"],
                "profile_id": file_details["ProfileID"],
                "profile_name": file_details["ProfileName"],
                "indexes": [
                    {"index": index["Index"], "index_value": index["IndexValue"]}
                    for index in file_details["ListOfIndexes"]["Indexes"]
                ]
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get file details. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get file details. Status code: " + str(response.status_code))

def docsvault_get_file_details_by_location(token_id: str, api_url: str, location: str) -> dict:
    """
    Gets the file details by its name and location in Docsvault.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        location (str): The full path with name of file starting from cabinet name.

    Returns:
        dict: A dictionary containing the file's details.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "FileDetails/GetFileDetailsByLocation"
    params = {"TokenID": token_id, "Location": location}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the file details from the API response
            file_detail = response_dict["Docsvault"]["Result"]["FileDetail"]

            # Return the file details as a dictionary
            return {
                "file_id": file_detail["FileID"],
                "parent_id": file_detail["ParentID"],
                "file_name": file_detail["FileName"],
                "description": file_detail["Description"],
                "flag_name": file_detail["FlagName"],
                "file_size": file_detail["FileSize"],
                "doc_type": file_detail["DocType"],
                "pages": file_detail["Pages"],
                "version": file_detail["Version"],
                "version_note": file_detail["VersionNote"],
                "version_owner": file_detail["VersionOwner"],
                "version_owner_name": file_detail["VersionOwnerName"],
                "modified_date": file_detail["ModifiedDate"],
                "created_date": file_detail["CreatedDate"],
                "accessed_date": file_detail["AccessedDate"],
                "checked_out": file_detail["CheckedOut"],
                "checked_out_by": file_detail["CheckedOutBy"],
                "checked_out_by_name": file_detail["CheckedOutByName"],
                "owner_id": file_detail["OwnerID"],
                "owner_name": file_detail["OwnerName"],
                "location": file_detail["Location"],
                "doc_notes": file_detail["DocNotes"],
                "profile_id": file_detail["ProfileID"],
                "profile_name": file_detail["ProfileName"],
                "list_of_indexes": file_detail.get("ListOfIndexes", {}).get("Indexes", [])
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get file details. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get file details. Status code: " + str(response.status_code))

def docsvault_get_file_profile(token_id: str, api_url: str, file_id: str) -> dict:
    """
    Gets the profile and index values of a file by its File ID.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        file_id (str): The unique ID of the file.

    Returns:
        dict: A dictionary containing the file's profile and index values.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "FileDetails/GetFileProfile"
    params = {"TokenID": token_id, "FileID": file_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the profile and index values from the API response
            file_detail = response_dict["Docsvault"]["Result"]["FileDetail"]
            indexes = file_detail.get("ListOfIndexes", {}).get("Indexes", [])
            index_values = {index["Index"]: index["IndexValue"] for index in indexes}

            # Return the profile and index values as a dictionary
            return {
                "flag_name": file_detail["FlagName"],
                "doc_notes": file_detail["DocNotes"],
                "profile_name": file_detail["ProfileName"],
                "index_values": index_values
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get file profile. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get file profile. Status code: " + str(response.status_code))

def docsvault_get_checked_out_files_by_user(token_id: str, api_url: str, user_id: str = "") -> dict:
    """
    Gets the list of checked out files by User ID or for all users.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        user_id (str, optional): The unique ID of the user. Pass a blank string to get details for all users. Defaults to "".

    Returns:
        dict: A dictionary containing the list of checked out files.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "FileDetails/GetCheckedoutFilesByUser"
    params = {"TokenID": token_id, "UserID": user_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the list of checked out files from the API response
            file_details = response_dict["Docsvault"]["Result"].get("FileDetail", [])

            # If there is only one file, convert it to a list
            if isinstance(file_details, dict):
                file_details = [file_details]

            # Return the list of checked out files as a dictionary
            return {
                "checked_out_files": [
                    {
                        "file_id": file_detail["FileID"],
                        "parent_id": file_detail["ParentID"],
                        "file_name": file_detail["FileName"],
                        "description": file_detail["Description"],
                        "flag_name": file_detail["FlagName"],
                        "file_size": file_detail["FileSize"],
                        "doc_type": file_detail["DocType"],
                        "pages": file_detail["Pages"],
                        "version": file_detail["Version"],
                        "version_note": file_detail["VersionNote"],
                        "version_owner": file_detail["VersionOwner"],
                        "version_owner_name": file_detail["VersionOwnerName"],
                        "modified_date": file_detail["ModifiedDate"],
                        "created_date": file_detail["CreatedDate"],
                        "accessed_date": file_detail["AccessedDate"],
                        "checked_out": file_detail.get("CheckedOut") == "true",
                        "checked_out_by": file_detail.get("CheckedOutBy", ""),
                        "checked_out_by_name": file_detail.get("CheckedOutByName", ""),
                        "owner_id": file_detail["OwnerID"],
                        "owner_name": file_detail["OwnerName"],
                        "location": file_detail["Location"]
                    }
                    for file_detail in file_details
                ]
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get checked out files. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get checked out files. Status code: " + str(response.status_code))

def docsvault_get_file_versions(token_id: str, api_url: str, file_id: str) -> dict:
    """
    Gets file versions by File ID.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        file_id (str): The unique ID of the file.

    Returns:
        dict: A dictionary containing the list of file versions.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """
    
    # Set the API action and parameters
    action = "FileDetails/GetFileVersion"
    params = {"TokenID": token_id, "FileID": file_id}
    
    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action
    
    # Send the API request
    response = requests.get(full_api_url, params=params)
    
    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)
        
        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the list of file versions from the API response
            file_details = response_dict["Docsvault"]["Result"].get("FileDetail", [])
            
            # If there is only one file version, convert it to a list
            if isinstance(file_details, dict):
                file_details = [file_details]
            
            # Return the list of file versions as a dictionary
            return {
                "file_versions": [
                    {
                        "file_size": file_detail["FileSize"],
                        "version": file_detail["Version"],
                        "version_note": file_detail["VersionNote"],
                        "version_owner": file_detail["VersionOwner"],
                        "version_owner_name": file_detail["VersionOwnerName"],
                        "created_date": file_detail["CreatedDate"],
                        "version_notes": file_detail["VersionNotes"]
                    }
                    for file_detail in file_details
                ]
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get file versions. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get file versions. Status code: " + str(response.status_code))

def docsvault_get_file_relations(token_id: str, api_url: str, file_id: str) -> dict:
    """
    Gets related documents by File ID.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        file_id (str): The unique ID of the file.

    Returns:
        dict: A dictionary containing the details of the related documents.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "FileDetails/GetFileRelations"
    params = {"TokenID": token_id, "FileID": file_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the details of the related documents from the API response
            file_details = response_dict["Docsvault"]["Result"].get("FileDetail", [])

            # If there is only one related document, convert it to a list
            if isinstance(file_details, dict):
                file_details = [file_details]

            # Return the details of the related documents as a dictionary
            return {
                "related_documents": [
                    {
                        "file_id": file_detail["FileID"],
                        "description": file_detail["Description"],
                        "location": file_detail["Location"]
                    }
                    for file_detail in file_details
                ]
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get related documents. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get related documents. Status code: " + str(response.status_code))

def docsvault_get_folder_details_by_id(token_id: str, api_url: str, folder_id: str) -> dict:
    """
    Gets folder details by folder ID.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        folder_id (str): The unique ID of the folder.

    Returns:
        dict: A dictionary containing the details of the folder.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "FolderDetails/GetFolderDetailsByID"
    params = {"TokenID": token_id, "FolderID": folder_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the folder details from the API response
            folder_detail = response_dict["Docsvault"]["Result"].get("FolderDetail", {})

            # Return the folder details as a dictionary
            return {
                "folder_id": folder_detail.get("FolderID"),
                "parent_id": folder_detail.get("ParentID"),
                "folder_name": folder_detail.get("FolderName"),
                "description": folder_detail.get("Description"),
                "flag_name": folder_detail.get("FlagName"),
                "has_child": folder_detail.get("HasChild"),
                "modified_date": folder_detail.get("ModifiedDate"),
                "created_date": folder_detail.get("CreatedDate"),
                "accessed_date": folder_detail.get("AccessedDate"),
                "checked_out": folder_detail.get("CheckedOut"),
                "checked_out_by": folder_detail.get("CheckedOutBy"),
                "checked_out_by_name": folder_detail.get("CheckedOutByName"),
                "owner_id": folder_detail.get("OwnerID"),
                "owner_name": folder_detail.get("OwnerName"),
                "location": folder_detail.get("Location"),
                "doc_notes": folder_detail.get("DocNotes"),
                "profile_id": folder_detail.get("ProfileID"),
                "profile_name": folder_detail.get("ProfileName"),
                "list_of_indexes": [
                    {
                        "index": index.get("Index"),
                        "index_value": index.get("IndexValue")
                    }
                    for index in folder_detail.get("ListOfIndexes", {}).get("Indexes", [])
                ]
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get folder details. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get folder details. Status code: " + str(response.status_code))

def docsvault_get_folder_details_by_location(token_id: str, api_url: str, location: str) -> dict:
    """
    Gets folder details by folder location.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        location (str): Full path and name of folder starting from cabinet name.

    Returns:
        dict: A dictionary containing the details of the folder.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "FolderDetails/GetFolderDetailsByLocation"
    params = {"TokenID": token_id, "Location": location}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the folder details from the API response
            folder_detail = response_dict["Docsvault"]["Result"].get("FolderDetail", {})

            # Return the folder details as a dictionary
            return {
                "folder_id": folder_detail.get("FolderID"),
                "parent_id": folder_detail.get("ParentID"),
                "folder_name": folder_detail.get("FolderName"),
                "description": folder_detail.get("Description"),
                "flag_name": folder_detail.get("FlagName"),
                "has_child": folder_detail.get("HasChild"),
                "modified_date": folder_detail.get("ModifiedDate"),
                "created_date": folder_detail.get("CreatedDate"),
                "accessed_date": folder_detail.get("AccessedDate"),
                "checked_out": folder_detail.get("CheckedOut"),
                "checked_out_by": folder_detail.get("CheckedOutBy"),
                "checked_out_by_name": folder_detail.get("CheckedOutByName"),
                "owner_id": folder_detail.get("OwnerID"),
                "owner_name": folder_detail.get("OwnerName"),
                "location": folder_detail.get("Location"),
                "doc_notes": folder_detail.get("DocNotes"),
                "profile_id": folder_detail.get("ProfileID"),
                "profile_name": folder_detail.get("ProfileName"),
                "list_of_indexes": [
                    {
                        "index": index.get("Index"),
                        "index_value": index.get("IndexValue")
                    }
                    for index in folder_detail.get("ListOfIndexes", {}).get("Indexes", [])
                ]
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get folder details. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get folder details. Status code: " + str(response.status_code))

def docsvault_get_folder_profile(token_id: str, api_url: str, folder_id: str) -> dict:
    """
    Gets the folder profile and corresponding index values by folder ID.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        folder_id (str): The unique ID of the folder.

    Returns:
        dict: A dictionary containing the folder profile and index values.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "FolderDetails/GetFolderProfile"
    params = {"TokenID": token_id, "FolderID": folder_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the folder profile and index values from the API response
            folder_detail = response_dict["Docsvault"]["Result"].get("FolderDetail", {})

            # Return the folder profile and index values as a dictionary
            return {
                "flag_name": folder_detail.get("FlagName"),
                "doc_notes": folder_detail.get("DocNotes"),
                "profile_name": folder_detail.get("ProfileName"),
                "list_of_indexes": [
                    {
                        "index": index.get("Index"),
                        "index_value": index.get("IndexValue")
                    }
                    for index in folder_detail.get("ListOfIndexes", {}).get("Indexes", [])
                ]
            }
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get folder profile. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get folder profile. Status code: " + str(response.status_code))

def docsvault_get_folder_relations(token_id: str, api_url: str, folder_id: str) -> dict:
    """
    Gets related documents by Folder ID.

    Args:
        token_id (str): The unique session ID.
        api_url (str): The Docsvault API endpoint URL.
        folder_id (str): Unique Folder ID.

    Returns:
        dict: A dictionary containing the details of the related documents.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
        ValueError: If the API response did not contain any data or if the response status code was not 200.
    """

    # Set the API action and parameters
    action = "FolderDetails/GetFolderRelations"
    params = {"TokenID": token_id, "FolderID": folder_id}

    # Construct the full API URL
    full_api_url = api_url.rstrip("/") + "/DocsvaultAPI/" + action

    # Send the API request
    response = requests.get(full_api_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the API response XML
        response_xml = response.content
        response_dict = xmltodict.parse(response_xml)

        # Check for any API errors
        if response_dict["Docsvault"]["Response"]["StatusCode"] == "0":
            # Extract the related documents from the API response
            related_docs = response_dict["Docsvault"]["Result"].get("RelatedDocs", {}).get("Doc", [])

            # Return the related documents as a list of dictionaries
            return [
                {
                    "doc_id": doc.get("DocID"),
                    "doc_name": doc.get("DocName"),
                    "doc_type": doc.get("DocType"),
                    "version": doc.get("Version"),
                    "folder_id": doc.get("FolderID"),
                    "folder_name": doc.get("FolderName"),
                    "location": doc.get("Location"),
                    "modified_date": doc.get("ModifiedDate"),
                    "created_date": doc.get("CreatedDate"),
                    "accessed_date": doc.get("AccessedDate"),
                    "size": doc.get("Size"),
                    "extension": doc.get("Extension"),
                    "checksum": doc.get("Checksum"),
                    "pages": doc.get("Pages"),
                    "author": doc.get("Author"),
                    "title": doc.get("Title"),
                    "subject": doc.get("Subject"),
                    "keywords": doc.get("Keywords"),
                    "category": doc.get("Category"),
                    "status": doc.get("Status"),
                    "comment": doc.get("Comment"),
                    "owner_id": doc.get("OwnerID"),
                    "owner_name": doc.get("OwnerName"),
                    "file_path": doc.get("FilePath"),
                    "doc_notes": doc.get("DocNotes"),
                    "workflow_status": doc.get("WorkflowStatus"),
                    "web_access": doc.get("WebAccess"),
                    "task_id": doc.get("TaskID")
                }
                for doc in related_docs
            ]
        else:
            error_message = response_dict["Docsvault"]["Response"]["Message"]
            raise ValueError("Could not get related documents. " + error_message)
    else:
        raise requests.exceptions.RequestException("Could not get related documents. Status code: " + str(response.status_code))
