from main import arrange_raw_eijirou


def describe_arrange_raw_eijirou():
    def describe_parse_correctlly():
        def test_non_tag_normal_pattern():
            test_data = ["■test-data : テストデータです"]
            actual = arrange_raw_eijirou(test_data)
            assert actual == {"test-data": ["テストデータです"]}
    
        def test_tag_normal_pattern():
            test_data = ["■test-data  {名} : テストデータです"]
            actual = arrange_raw_eijirou(test_data)
            assert actual == {"test-data": ["[名] テストデータです"]}

        def test_multi_same_word_pattern():
            test_data = [
                "■test-data  {名-1} : テストデータ1です",
                "■test-data  {名-2} : テストデータ2です",
                "■test-data : 【レベル】1。テストのレベルです"
            ]
            actual = arrange_raw_eijirou(test_data)
            assert actual == {"test-data": [
                "[名-1] テストデータ1です",
                "[名-2] テストデータ2です",
                "【レベル】1。テストのレベルです"
            ]}
        
        def test_composit_pattern():
            test_data = [
                "■test-data  {名-1} : テストデータ1です",
                "■test-data  {名-2} : テストデータ2です",
                "■test-data : 【レベル】1。テストのレベルです",
                "■hogehoge : ホゲホゲ"
            ]
            actual = arrange_raw_eijirou(test_data)
            assert actual == {
                "test-data": [
                    "[名-1] テストデータ1です",
                    "[名-2] テストデータ2です",
                    "【レベル】1。テストのレベルです"
                ],
                "hogehoge": ["ホゲホゲ"]
            }




