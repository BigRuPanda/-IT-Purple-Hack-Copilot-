# Импорт библиотек и классов
import aiosqlite

# Класс БД
class DataBase:

    # Инит БД
    def __init__(self, db_file: str):
        """
        Initialize database class

        Args:
            db_file (str): database file path
        """
        self.db_file = db_file

    # Работа с пользователем
    async def add_user(self, user_id: str):
        """
        Add user in database

        Args:
            user_id (str): Telegram user id in database
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            await connection.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))
            await connection.commit()

    async def user_exists(self, user_id: str):
        """
        Check if user exists in database

        Args:
            user_id (str): Telegram user id in database

        Returns:
            bool: boolean value whether the user exists
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            cursor = await connection.execute("SELECT * FROM 'users' WHERE user_id = ?", (user_id,))
            result = await cursor.fetchall()
            return bool(len(result))


    # Работа с ассистентом
    async def set_assistent(self, user_id: str, assistent: str):
        """
        Set the assistant type for the user in database

        Args:
            user_id (str): Telegram user id in database
            assistent (str): Assistent type name:
            - 'multipurpose'
            - 'designer'
            - 'stylist'
            - 'cosmetologist'
            - 'nutritionist'
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            await connection.execute("UPDATE 'users' SET assistent = ? WHERE user_id = ?", (assistent, user_id,))
            await connection.commit()

    async def get_assistent(self, user_id: str):
        """
        Get the assistant type from the user

        Args:
            user_id (str): Telegram user id in database

        Returns:
            str: Assistent type name
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            cursor = await connection.execute("SELECT assistent FROM 'users' WHERE user_id = ?", (user_id,))
            result = await cursor.fetchall()
            for row in result:
                assistent = str(row[0])
            return assistent


    # Работа с гендером
    async def set_gender(self, user_id: str, gender: str):
        """
        Set the gender for the user in database

        Args:
            user_id (str): Telegram user id in database
            gender (str): Gender name:
            - 'male'
            - 'female'
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            await connection.execute("UPDATE 'users' SET gender = ? WHERE user_id = ?", (gender, user_id,))
            await connection.commit()
        
    async def get_gender(self, user_id: str):
        """
        Get the gender name from the user

        Args:
            user_id (str): Telegram user id in database

        Returns:
            str: Gender name
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            cursor = await connection.execute("SELECT gender FROM 'users' WHERE user_id = ?", (user_id,))
            result = await cursor.fetchall()
            for row in result:
                gender = str(row[0])
            return gender


    # Работа с возрастом
    async def set_age(self, user_id: str, age: str):
        """
        Set the age for the user in database

        Args:
            user_id (str): Telegram user id in database
            age (str): User's age
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            await connection.execute("UPDATE 'users' SET age = ? WHERE user_id = ?", (age, user_id,))
            await connection.commit()
    
    async def get_age(self, user_id: str):
        """
        Get the age from the user

        Args:
            user_id (str): Telegram user id in database

        Returns:
            str: User's age
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            cursor = await connection.execute("SELECT age FROM 'users' WHERE user_id = ?", (user_id,))
            result = await cursor.fetchall()
            for row in result:
                age = str(row[0])
            return age
        

    # Работа с бюджетом
    async def set_budget(self, user_id: str, budget: str):
        """
        Set the budget for the user in database

        Args:
            user_id (str): Telegram user id in database
            budget (str): User's budget
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            await connection.execute("UPDATE 'users' SET budget = ? WHERE user_id = ?", (budget, user_id,))
            await connection.commit()

    async def get_budget(self, user_id: str):
        """
        Get the budget from the user

        Args:
            user_id (str): Telegram user id in database

        Returns:
            str: User's budget
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            cursor = await connection.execute("SELECT budget FROM 'users' WHERE user_id = ?", (user_id,))
            result = await cursor.fetchall()
            for row in result:
                budget = str(row[0])
            return budget


    # Работа с дополнительной информацией
    async def set_info(self, user_id: str, info: str):
        """
        Set the info about user's request in database

        Args:
            user_id (str): Telegram user id in database
            info (str): Info about user's request
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            await connection.execute("UPDATE 'users' SET info = ? WHERE user_id = ?", (info, user_id,))
            await connection.commit()

    async def get_info(self, user_id: str):
        """
        Get the info about user's request in database

        Args:
            user_id (str): Telegram user id in database

        Returns:
            str: Info about user's request
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            cursor = await connection.execute("SELECT info FROM 'users' WHERE user_id = ?", (user_id,))
            result = await cursor.fetchall()
            for row in result:
                info = str(row[0])
            return info


    # Работа с товарами в корзине
    async def set_goods(self, user_id: str, goods: str):
        """
        Add IDs of items in the user's cart to the database

        Args:
            user_id (str): Telegram user id in database
            goods (str): IDs of items in the user's cart
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            await connection.execute("UPDATE 'users' SET goods = ? WHERE user_id = ?", (goods, user_id,))
            await connection.commit()

    async def get_goods(self, user_id: str):
        """
        Get IDs of items in the user's cart to the database

        Args:
            user_id (str): Telegram user id in database

        Returns:
            str: IDs of items in the user's cart
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            cursor = await connection.execute("SELECT goods FROM 'users' WHERE user_id = ?", (user_id,))
            result = await cursor.fetchall()
            for row in result:
                goods = str(row[0])
            return goods


    # Работа с объяснениями
    async def set_messages(self, user_id: str, messages: str):
        """
        Set assistent's messages for items in the user's cart to the database

        Args:
            user_id (str): Telegram user id in database
            messages (str): assistent's messages for items in the user's cart
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            await connection.execute("UPDATE 'users' SET messages = ? WHERE user_id = ?", (messages, user_id,))
            await connection.commit()

    async def get_messages(self, user_id: str):
        """
        Get assistent's messages for items in the user's cart to the database

        Args:
            user_id (str): Telegram user id in database

        Returns:
            str: assistent's messages for items in the user's cart
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            cursor = await connection.execute("SELECT messages FROM 'users' WHERE user_id = ?", (user_id,))
            result = await cursor.fetchall()
            for row in result:
                messages = str(row[0])
            return messages


    # Работа с проверкой жив/мертв
    async def set_alive(self, user_id: str):
        """
        Set alive (1) status to the user in database.

        Args:
            user_id (str): Telegram user id in database
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            await connection.execute("UPDATE 'users' SET alive = 1 WHERE user_id = ?", (user_id,))
            await connection.commit()
    
    async def set_dead(self, user_id: str):
        """
        Set dead (0) status to the user in database.

        Args:
            user_id (str): Telegram user id in database
        """        
        async with aiosqlite.connect(self.db_file) as connection:
            await connection.execute("UPDATE 'users' SET alive = 0 WHERE user_id = ?", (user_id,))
            await connection.commit()