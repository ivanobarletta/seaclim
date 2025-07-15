# Common functions and error handling for SeaClim workflow

# Function to check if directory exists
check_directory() {
    if [ ! -d "$1" ]; then
        echo "ERROR: Directory not found: $1"
        exit 1
    fi
}

# Function to create directory with error checking  
safe_mkdir() {
    mkdir -p "$1"
    if [ $? -ne 0 ]; then
        echo "ERROR: Could not create directory: $1"
        exit 1
    fi
}

sed_namelist () {
    # this function creates the namelist_cfg
    # from the template namelist_cfg_template
         
    template_nml=$1
    new_nml=$2

    SED_REPLACEMENTS=(
    "s/{MEMBER}/${MEMBER}/g"   
    "s/{HINDCAST_YEAR}/${HINDCAST_YEAR}/g"
    "s/{CYCLE_NUMBER}/${CYCLE_NUMBER}/g"             
    "s/{NN_IT000}/${NN_IT000}/g"
    "s/{NN_ITEND}/${NN_ITEND}/g"
    "s/{NN_DATE0}/${NN_DATE0}/g"
    )

    SED_ARGS=""
    for replacement in "${SED_REPLACEMENTS[@]}"; do
        SED_ARGS="${SED_ARGS} -e ${replacement}"
    done

    sed ${SED_ARGS} ${template_nml} > ${new_nml}
}

next_month() {
    local current_month_str="$1"
    local current_month_int

    # Check if an argument is provided.
    if [ -z "$current_month_str" ]; then
        echo "Error: No month provided. Usage: next_month <month_number>" >&2
        return 1
    fi

    # Convert the input string to an integer, removing any leading zeros.
    # This ensures that "01" is treated as 1, and "10" as 10 for arithmetic.
    current_month_int=$(echo "$current_month_str" | sed 's/^0*//')

    # Validate if the input is a valid number between 1 and 12.
    if ! [[ "$current_month_int" =~ ^[0-9]+$ ]] || (( current_month_int < 1 || current_month_int > 12 )); then
        echo "Error: Invalid month number '$current_month_str'. Please provide a number between 1 and 12." >&2
        return 1
    fi

    local next_month_int

    # Calculate the next month by adding 1.
    next_month_int=$((current_month_int + 1))

    # If the next month is greater than 12, reset it to 1 (January).
    if (( next_month_int > 12 )); then
        next_month_int=1
    fi

    # Print the result, formatted to always be two digits (e.g., 1 becomes 01, 10 remains 10).
    # double %% is necessary for proper conversion to .ecf
    printf "%%02d\n" "$next_month_int"  
}

previous_cycle() {
    local input_cycle="$1"

    if [ "${input_cycle}" -eq "00" ]; then 
        echo "Error. previous_cycle(). You cannot provide 00"
        echo "       As input"
        exit 1 
    fi    
    prev_cycle=$((input_cycle - 1))
    printf "%%02d\n" "${prev_cycle}"
}

next_cycle() {
    local input_cycle=$1
    next_cycle=$((input_cycle + 1))
    printf "%%02d\n" "${next_cycle}"
}


# Set common environment
export LANG=C
export LC_ALL=C
