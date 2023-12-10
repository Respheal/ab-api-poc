const baseUrl = process.env.API_BASE_PATH;

/**
 * Output a string of key-value pairs in the format of a query string.
 * @param {Object} obj  Key-value pairs to convert to a query string.
 */
function objectToQueryString(obj) {
    const keys = Object.keys(obj);
    const keyValuePairs = keys.map((key) => {
        return encodeURIComponent(key) + "=" + encodeURIComponent(obj[key]);
    });
    return keyValuePairs.join("&");
}

/**
 * User-specific endpoint functions
 */
const User = {
    /**
     * Given user data, search the API for a single user matching data.
     * @param {Object} userData  Key-value pairs with which to search the API.
     */
    async searchUser(userData) {
        try {
            const response = await fetch(
                `${baseUrl}/users/?${objectToQueryString(userData)}`,
                { method: "GET" }
            );
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const data = await response.json();
            if (data && data[0]) {
                return data[0];
            }
        } catch (error) {
            console.error("Error:", error);
        }
    },
    async createUser(userData) {
        try {
            const response = await fetch(`${baseUrl}/users/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(userData),
            });

            const result = await response.json();
            console.log("Success:", result);
        } catch (error) {
            console.error("Error:", error);
        }
    },
};

export default User;
