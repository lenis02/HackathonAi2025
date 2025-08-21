import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(String, index=True)
    source_key = Column(String, index=True)
    ts = Column(DateTime)
    ac_power = Column(Float)

Base.metadata.create_all(bind=engine)

def import_csv_to_db(csv_path):
    db = SessionLocal()
    try:
        print(f"'{csv_path}' 파일에서 과거 데이터를 불러옵니다...")
        df = pd.read_csv(csv_path)

        # 'DATE_TIME' 컬럼을 'ts'로 이름을 변경하고 datetime 객체로 변환
        df.rename(columns={'DATE_TIME': 'ts'}, inplace=True)
        df['ts'] = pd.to_datetime(df['ts'])
        
        # 데이터가 너무 많을 수 있으므로 최신 데이터 일부만 사용 (예: 5000개)
        # 전체를 넣어도 되지만 시간이 오래 걸릴 수 있습니다.
        df = df.sort_values(by='ts').tail(5000)
        
        records_to_add = []
        for _, row in df.iterrows():
            record = Prediction(
                plant_id=str(row['PLANT_ID']),
                source_key=row['SOURCE_KEY'],
                ts=row['ts'],
                ac_power=row['AC_POWER'] # 컬럼명을 AC_POWER로 수정
            )
            records_to_add.append(record)
            
        db.add_all(records_to_add)
        db.commit()
        
        print(f"✅ 성공적으로 {len(records_to_add)}개의 과거 데이터를 DB에 저장했습니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # generation_train.csv 파일을 읽도록 경로 설정
    import_csv_to_db('generation_train.csv')