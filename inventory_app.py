#!/usr/bin/env python

from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, send_file
from item_manipulations import put_item, delete_item_func, query_items, get_item, scan_items, print_items, update_item, get_inventory_from_search

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

def format_item(item)->dict:
    """Takes one item from the inventory as input and returns a dictionary with all attributes outside of the information dict."""
    attrs = ['item_name',
            'item_id']

    item_dict = {}

    for key in attrs:
        item_dict[key] = item[key]

    for attr in item['info']:
        item_dict[attr] = item['info'][attr]

    return item_dict

# Formats entire inventory list
def format_inventory(inventory: list[(dict)])->list[dict]:
    """returns the inventory in a parse-friendly format"""
    inventory_arr = []

    for item in inventory:
        inventory_arr.append(format_item(item))

    return inventory_arr

def is_none(a):
    """
    returns empty string when input is a None value
    otherwise returns input
    """
    if a is not None:
        return a
    else:
        return ""

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():    
    show_open = True

    rule = request.url_rule

    if 'search' in rule.rule:
        search_term = request.args.get('q')
        inventory = get_inventory_from_search(is_none(search_term))
    else:
        inventory = scan_items()

    if 'index' in rule.rule:
        search_term = request.args.get('q')
        if search_term == "closed":
            show_open = False

    inventory_arr = None if len(inventory) == 0 else format_inventory(inventory)


    html = render_template('index.html',
        inventory_arr=inventory_arr,
        show_open = show_open)
    response = make_response(html)
    return response

@app.route('/search', methods=['GET'])
def search():
    
    search_term = request.args.get('q')

    print(f"search term: {search_term}")
    inventory = get_inventory_from_search(is_none(search_term))
    inventory_arr = None or format_inventory(inventory)

    # Make separate arrays of sold out items and available items
    sold_out = request.args.get('Sold_Out')
    print(sold_out)
    if sold_out:
        if sold_out == 'True':
            inventory_arr = [item for item in inventory_arr if item['Sold_Out'] == 'True']
        else:
            inventory_arr = [item for item in inventory_arr if item['Sold_Out'] == 'False']
        pass

    html = ''

    # Make cards for search available
    for item in inventory_arr:
        html += f'''
        <div class="col">
            <div class="card mb-4 rounded-3 shadow-sm h-100">

                <div class="card-body">
                    <h5 class="card-title">{ item['item_name'] }<small class="text-muted fw-light">, Item No:</small>{ item['item_id'] }</h5>
                    <p class="card-subtitle mb-2 text-muted"> Color: { item['Color'] or "NA" }</p>
                    <p class="card-subtitle mb-2 text-muted"> Length: { item['Length'] or "NA" }"</p>
                    <p class="card-subtitle mb-2 text-muted"> Fabric: { item['Fabric'] or "NA" }</p>
                </div>
                <div class="card-footer">
                    {"Item is currently available" if item['Sold_Out']=="False" else "Item is sold out" }
                </div>
                <a href="details?item_name={ item['item_name'] }&item_id={item['item_id']}" class="stretched-link"></a>
                
            </div>
        </div>
        
        '''
    response = make_response(html)

    return response

@app.route('/details', methods=['GET'])
def details():

    item = get_item(request.args['item_name'], int(request.args['item_id']))
    item = format_item(item)
    attr_list = ['Color', 'Length', 'Fabric', 'Sold_Out']
    html = render_template('item.html',
        item=item, attr_list = attr_list)
    response = make_response(html)
    return response

@app.route('/add_item', methods=['POST'])
def add_item():
    item_info_titles = ["item_name", "item_id","color","length", "fabric"]
    item_info = []
    for i in item_info_titles:
        try:
            item_info.append(request.form.get(i))
        except:
            item_info.append("")

    assert(len(item_info)==len(item_info_titles))

    put_item(item_info[0], int(item_info[1]), item_info[2], int(item_info[3]), item_info[4])
    return redirect(url_for("index"))

@app.route('/delete/<name>/<id>')
def delete_item(name, id):
    item_name = name
    item_id = id
    delete_item_func(item_name, int(item_id))
    return redirect(url_for("index"))

@app.route('/updateitem/<name>/<id>', methods=['POST'])
def update_item_by_name_id(name, id):
    color = request.form.get("color")
    sold_out = request.form.get("sold_out")
    item_name = name
    item_id = id
    update_item(item_name, int(item_id), color, sold_out)
    return redirect(url_for('details', item_name = item_name, item_id = item_id))

