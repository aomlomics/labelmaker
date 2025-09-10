## Instructions for Southeast US MBON eDNA Sample Labels

Use the files `sample_list_mbon_1-28.txt`, `sample_list_mbon_29-56.txt`, and `sample_list_mbon_57-84.txt` in this directory to create labels for up to 84 samples including triplicates.

From the main labelmaker directory, run the command below. Change the project to reflect the correct cruise ID (2 letters for ship name, 2 numbers for year, 3 numbers for ordinal date), and change the date to reflect the starting month and year of the cruise.

```bash
./generate_labels.py --project WSYYDDD --contact Montes --date Jan-YYYY --sample_list user-seusmbon/sample_list_mbon_1-28.txt --separator '-'
```

For additional sheets, run the command again with the other sample lists.

It is recommended to print a test sheet on regular paper, then align it with a label sheet to see how it looks, before printing on the more expensive label sheets. 
