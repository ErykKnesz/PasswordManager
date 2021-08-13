import sql
import menu


if __name__ == '__main__':
    sql.create_database()
    conn = sql.create_connection(r"PasswordManager")
    sql.create_table(conn)
    is_on = True
    while is_on:
        rows = sql.select_all(conn)
        for name in rows:
            print(f"Your database includes passwords for: \n - {name[1]}",
                  end="\n")
        option = menu.ask_for_prompt()
        if option == 0:
            conn.close()
            menu.perform_desired_action(conn, option)
            is_on = False
        menu.perform_desired_action(conn, option)

