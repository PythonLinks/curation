from dolmen.container import IBTreeContainer


def size(item):
    result=1
    if IBTreeContainer.providedBy(item):
        for child  in item.values():
            result+=size(child)
    return result


    
