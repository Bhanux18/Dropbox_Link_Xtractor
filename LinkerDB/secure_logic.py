
import dropbox

def traverse_folder(dbx, folder_path, main_folder, subfolder="", file_types=None):
    image_links = []
    try:
        result = dbx.files_list_folder(folder_path)
    except Exception as e:
        return []

    for entry in result.entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            image_links += traverse_folder(dbx, entry.path_display, main_folder, subfolder=entry.name, file_types=file_types)
        elif isinstance(entry, dropbox.files.FileMetadata):
            if file_types and not any(entry.name.lower().endswith(ft.lower()) for ft in file_types):
                continue
            try:
                link = dbx.sharing_create_shared_link(entry.path_display).url
            except Exception as e:
                try:
                    links = dbx.sharing_list_shared_links(path=entry.path_display)
                    link = links.links[0].url if links.links else None
                except:
                    continue
            if link:
                image_links.append({
                    'Main Folder': main_folder.strip('/'),
                    'Subfolder': subfolder,
                    'File Name': entry.name,
                    'Dropbox Share Link': link,
                    'Direct Embed Link': link.replace('?dl=0', '?raw=1')
                })
    return image_links
