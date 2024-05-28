
    def update_user(self, ids: int, **kwargs) -> None:
        ''' update a value '''
        u1 = self.find_user_by(id=ids)
        if u1 is None:
            return
        cols = {}
        for k, v in kwargs.items():
            if hasattr(User, k):
                cols[getattr(User, k)] = v
            else:
                raise ValueError()
        
        self._session.query(User).filter(User.id == ids).update(
            cols,
            synchronize_session=False,
        )
        self._session.commit()