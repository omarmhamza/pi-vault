db.createUser(
        {
            user: "user",
            pwd: "Pl6VuTfrqY",
            roles: [
                {
                    role: "readWrite",
                    db: "vault"
                }
            ]
        }
);