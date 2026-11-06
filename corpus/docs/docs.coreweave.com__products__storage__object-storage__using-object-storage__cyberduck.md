# Use Cyberduck with CoreWeave AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/using-object-storage/cyberduck

# Use Cyberduck with CoreWeave AI Object Storage

> How to manage CoreWeave AI Object Storage buckets and objects with Cyberduck

[Cyberduck](https://cyberduck.io/) is a desktop cloud storage browser that you can use to manage buckets and objects with AI Object Storage.

> [!TIP]
>
> For a lighter-weight, browser-based experience, you can also [manage objects from the Cloud Console](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects.md) without installing any software. Cyberduck remains a good option if you prefer a desktop application or need features such as bookmarks and **Transfers** window management.

## Prerequisites

* Obtain a CoreWeave AI Object Storage Access Key and Secret. If you don't already have these credentials, [generate them in the Cloud Console](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md).
* Set an [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md).
* [Download and install Cyberduck](https://cyberduck.io/download/).

## Installation and configuration

1. Open the Cyberduck application.

2. Install the CoreWeave AI Object Storage connection profile:

   * In Cyberduck's menu bar, locate **Connection Profiles**:
     * For macOS: **Cyberduck ▸ Settings ▸ Connection Profiles**.
     * For Windows: **Edit ▸ Preferences ▸ Connection Profiles**.
   * In the profiles gallery's search field, type "CoreWeave". Search results may take a few minutes to appear. You only need to complete this step once at initial setup.
   * Check the checkbox next to "CoreWeave AI Object Storage".
   * Close **Preferences**.
   * Restart Cyberduck (close and re-open the application) for the profile to appear persistently in the 'New Connection' dropdown list.

![Cyberduck connection profile](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/storage/_media/cd-connection-profile.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=187257371b949be38a48ebdc9bf05f41)

After you restart Cyberduck, the CoreWeave AI Object Storage connection profile is installed and available when you open a new connection.

## Connect to CoreWeave AI Object Storage

When you open a connection from Cyberduck to AI Object Storage, you have the option to save a bookmark for more convenient access, but it's not required.

### Open a connection

1. Click the **Open Connection** toolbar button (or **File ▸ Open Connection**).
2. Enter your CoreWeave AI Object Storage Access Key and Secret. For macOS, the "Add to Keychain" checkbox is selected by default at the bottom left. Uncheck this option if you prefer to enter your secret each time.

![Cyberduck connection with CoreWeave AI Object Storage](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/storage/_media/cd-connection.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=74dcc71f5da495037cee8cc7371c0750)

The Cyberduck browser displays a root-level view showing all your buckets.

You can [add a bookmark from your current connection](https://docs.cyberduck.io/cyberduck/bookmarks/#add-new-bookmark).

### Save a bookmark

Bookmarks allow you to save connection settings, like a default path. When you save a bookmark in Cyberduck, it remains in your main Cyberduck browser window, labeled with its nickname and your access key.

1. In Cyberduck, open the **Bookmark** menu and select **New Bookmark**.
2. Expand the dropdown menu at the top. Scroll to the bottom of the menu and select **CoreWeave AI Object Storage**.
3. Give the connection a nickname.
4. Optional: In macOS, you can create labels to organize and group your Cyberduck bookmarks.
5. Enter your CoreWeave AI Object Storage Access Key and Secret.
6. To bookmark your connection to a specific bucket, set your default path:
   * Expand **More Options**.
   * The **Path** field defaults to the root; append your bucket name. For example, `/test-bucket`.
7. Close the bookmark dialog window. Cyberduck saves the bookmark and displays it in the browser window.
8. Double-click your new bookmark. The Cyberduck browser reflects the path if you set one; otherwise it displays the root-level view of all your buckets.

![Cyberduck bookmark for CoreWeave AI Object Storage](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/storage/_media/cd-bookmark.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=46cc63f09c2c35eddef1d63c76ce33a8)

## Manage AI Object Storage resources

This section shows how to manage buckets and files in Cyberduck.

### Create a new bucket in CoreWeave AI Object Storage

1. Open your bookmark and make sure you are connected to AI Object Storage. If you see the bookmark name at the top of the window with your access key ID displayed below it (like `CWESGLIQGQWMAUXM@cwobject.com`), the connection is successful:

   ![Cyberduck root browser view](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/cd-root-view.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=301c5700b38ff45b0e660eadfbe29629)

2. Make sure no existing buckets are selected.

3. Expand the Cyberduck browser window to view the **Actions** menu (gear icon). Expand this menu, and click **New Folder**. (Alternatively, use **File > New Folder** from the main menu, or right-click and select **New Folder**.)

4. In the **Create new folder** dialog window, enter a name for your bucket and select the region.

   > [accordion] Bucket naming rules
   >
   > Bucket names must be globally unique and adhere to the following rules:
   >
   > * **Length:** 3 to 63 characters.
   > * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
   > * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
   > * **Prohibited patterns:** Cannot start with `xn--`.
   > * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

5. Click the **Create** button to create the bucket.

   If you're not prompted to select a region, you're creating a folder inside an existing bucket. Deselect any selected buckets before creating a new bucket.

   ![Cyberduck bucket creation](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/cd-create-bucket.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=c4a753fe44e83d49fcf02dd1dfd39777)

> [!WARNING]
>
> **Delay after bucket creation**
>
> Due to DNS caching, buckets created with Cyberduck may take several minutes to become available for use. If you try to use a bucket immediately after creating it, Cyberduck may show an error: `Region does not match. Please contact your web hosting service provider for assistance.` Wait a few minutes before adding folders or files to a newly created bucket.

### Create a new folder

To create a new folder within a bucket:

1. Select your bucket in the Cyberduck browser.
2. Using the main Cyberduck menu, go to **File > New Folder**. (Alternatively, expand the **Actions** menu on the Cyberduck browser and click **New Folder**, or right-click and select **New Folder**.)
3. Enter a name for the folder, and click **Create**:

   ![Cyberduck folder creation](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/cd-create-folder.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=6d0bc49dbf0d425b326f1f5e8e169310)

If you're prompted to select a region, you're creating a new bucket. To create a new folder within an existing bucket, make sure your bucket is selected in the Cyberduck browser before you create the folder.

### Upload files to the newly created bucket

1. Open your file explorer and browse to the files you want to upload.
2. Select the files and drag them into the Cyberduck window; hover over the newly created bucket until it is highlighted, and then drop in the files.
3. The **Transfers** window shows upload progress and status:

   ![Cyberduck transfers](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/cd-transfers.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=423f0474e4d602e09d18f9a7bd9e8fc3)

   It displays both the local file path and a path-style URL. The local path link opens the file in your file explorer. AI Object Storage doesn't support path-style URLs; they return an error.

### Browse and search files

To browse files within a bucket:

* In the root-level view, expand the carat next to the bucket name to view the subdirectories and objects.
* Alternatively, double-click the bucket and the Cyberduck browser shows only items in that bucket.

To search files within a bucket:

1. Double-click the bucket you want to search. You should now see a list of files in the bucket.
2. Click the **Search** icon at the top of the Cyberduck browser.
3. Enter a search term to find files by name. Click **Search** to confirm in the dialog window. After a few moments, the Cyberduck browser displays your search results.

![Cyberduck search](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/cd-search.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=9349a1ca2aa92db88899d9abce49442f)

### Delete resources

To delete files within a bucket:

1. Click into the bucket in the Cyberduck browser.
2. Select the files you want to delete. Use command-click or right-click and select **Delete**.
3. The dialog window lists the items to delete. Click the **Delete** button to confirm:

   ![Cyberduck delete dialog](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/cd-delete.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=8fa07f825b4530251781b7c02663bf69)

If you're in the root view that shows all buckets, be careful not to select entire buckets when deleting multiple items.

To delete buckets:

1. In the main Cyberduck browser, select the bucket(s) you want to delete.
2. Command-click or right click and select **Delete**.
3. The dialog window lists the items you wish to delete. Click the **Delete** button to confirm.

A bucket can only be deleted once it is completely empty: no current objects, no noncurrent versions, no delete markers, and no incomplete multipart uploads. Cyberduck does not list incomplete multipart uploads, which are the most common reason a delete attempt fails on a bucket that appears empty. For a complete cleanup procedure, see [Empty and delete a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/empty-and-delete-bucket.md).
