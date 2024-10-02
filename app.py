import streamlit as st
from typing import List, Optional

# Define the function to check planning permission based on various conditions
def requires_planning_permission(
    category: str, 
    location: str, 
    height: str, 
    constraints: Optional[List[str]] = None, 
    other_conditions: Optional[str] = None
) -> bool:
    """
    Determine if planning permission is required based on the site category and conditions.

    Args:
        category (str): Site category (e.g., '2U1', '2A3').
        location (str): Location of the fence, wall, or gate (e.g., 'adjacent').
        height (str): Height of the structure (e.g., 'up to 1m').
        constraints (List[str]): List of planning constraints (e.g., ['Listed building']).
        other_conditions (Optional[str]): Additional conditions (e.g., 'New build property').

    Returns:
        bool: True if planning permission is required, otherwise False.
    """
    # Universal categories that always require planning permission
    universal_categories = {'2U1', '2U2', '2U3', '2U4', '2U5', '2U6', '2U7', '2U8', '2U9'}
    
    # If the category is one of the universal categories, return True
    if category in universal_categories:
        return True

    # Define conditions for only 2A3 and 2A6 categories
    permission_matrix = {
        '2A3': {'Location': 'adjacent', 'Height': 'above 1m'},  # Permission required if location and height match
        '2A6': {'Location': 'face property', 'Height': 'above 2m'}  # Permission required if location and height match
    }
    
    # Check the conditions for 2A3 and 2A6 only
    if category in permission_matrix:
        conditions = permission_matrix[category]
        # Check constraints match for 2A3 and 2A6
        if location == conditions['Location']:
            if conditions['Height'] == "above 1m":
                if height > 1:
                    return True
            elif conditions['Height'] == "above 2m":
                if height > 2:
                    return True
    
    # If none of the conditions are met, planning permission is not required
    return False



st.title("Planning Permission Checker")


# User inputs for category, location, height, constraints, and other conditions
category = st.selectbox("Select Site Category:", ['2U1', '2U2', '2U3', '2U4', '2U5', '2U6', '2U7', '2U8', '2U9', '2A1', '2A3', '2A6'])
location = st.radio("Enter Location (e.g., 'adjacent', 'face property'):", ['adjacent', 'face property'])
height = st.slider("Enter Height (e.g., 'up to 1m', 'above 1m', 'above 2m'):", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
constraints = st.multiselect("Select Planning Constraints:", ['Listed building', 'Article 2(3) Land', 'Article 2(4) Land', 'Article 4 Directive', 'AONB', 'works affecting TPO'])
other_conditions = st.selectbox("Select Other Conditions:", 
                                ['Permitted', 'New build property - restrictions applied'],
                                index=None)


# Check if all mandatory fields are filled
if st.button("Check Planning Permission"):
    if category and location and height:
        # Call the planning permission function
        permission_required = requires_planning_permission(category, location, height, constraints, other_conditions)
        # Display the result
        if permission_required:
            st.error(f"Planning Permission is **required** for the site category '{category}' with the given conditions.")
        else:
            st.success(f"Planning Permission is **not required** for the site category '{category}' with the given conditions.")
    else:
        st.error("Please fill in all mandatory fields (Category, Location, and Height).")

