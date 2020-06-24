This tool convert CSV files to JSON files.

The missing dialogues are logged in the `missing.txt` file.

Run the tool with `python CSVtoJSON.py -c input_csv -j output_json`

Additional command-line options:<br>
`-p, --prefix` - change the dialogue prefix, default: TEXT<br>
`-rl, --remove_lines` - change the number of lines removed in the header, default: 2