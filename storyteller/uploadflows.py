from metaflow import FlowSpec, step, IncludeFile, Parameter


class UploadWisdoms(FlowSpec):

    def start(self):
        """
        set ver to be available
        """
        pass

    def dl_from_sheet(self):
        """
        ver  -> all_df
        """
        pass

    def package(self):
        """
        all_df -> all_table -> wisdoms_artifact
        """
        pass

    def end(self):
        # upload the artifact
        pass


class UploadWisdom2Query(FlowSpec):

    def start(self):
        """
        set ver to be available
        """
        pass

    def dl_from_sheet(self):
        """
        ver  -> raw_df
        """
        pass

    def preprocess(self):
        """
        raw_df -> all_df
        """
        pass

    def val_test_split(self):
        """
        all_df -> val_df, test_df
        """
        pass

    def package(self):
        """
        raw_df, all_df, val_df, test_df -> wisdom2query_artifact
        """
        pass

    def end(self):
        """
        upload the artifact
        :return:
        """
        pass


class UploadWisdom2Def(FlowSpec):

    def start(self):
        """
        set ver to be available
        """
        pass

    def dl_from_sheet(self):
        """
        ver  -> raw_df
        """
        pass

    def preprocess(self):
        """
        raw_df -> all_df
        """
        pass

    def package(self):
        """
        raw_df, all_df -> wisdom2def_artifact
        """
        pass

    def end(self):
        """
        upload the artifact
        """
        pass


class UploadWisdom2Eg(FlowSpec):

    def start(self):
        """
        set ver to be available
        """
        pass

    def search_on_indices(self):
        """
        ver -> raw_df
        """
        pass

    def preprocess(self):
        """
        raw_df -> all_df
        """
        pass

    def package(self):
        """
        raw_df, all_df -> wisdom2eg_artifact
        """
        pass

    def end(self):
        """
        upload the artifact
        """
        pass
